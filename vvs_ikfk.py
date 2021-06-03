# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.OpenMayaUI as omui
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import maya.mel as mel
import shiboken2.wrapInstance as wrp


# this is universal rig ikfk tool.
# First you need to setup your rig. Via UI "create_ui()" or via "setup_save(*args)" function if you know what to save. All information will be stored in config nodes.
# The to switch ik/fk you need to select control and run:
# ikfk_obj = IKFK()
# ikfk_obj.switcher()


ikfk_setup_win = None


# gettin maya window
def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrp(long(ptr), QtWidgets.QMainWindow)


# 0. ********* Класс для линковки и сопоставления объектов в пространстве ****************************************************************************
def get_hier_transformation(control_str):
    control = pm.PyNode(control_str)
    hier = []
    for s in control.fullPath().split("|")[1:-1]:
        hier.append(pm.PyNode(s))
    hier.reverse()
    res_m = pm.datatypes.TransformationMatrix()
    for node in hier:
        res_m *= node.getTransformation()
    return res_m


class ObjLinker():
    def __init__(self, obj_a_str, obj_b_str, pre_setuped_matrix=None):
        self.a = pm.PyNode(obj_a_str)
        self.b = pm.PyNode(obj_b_str)
        if pre_setuped_matrix:
            self.relative_matrix = pre_setuped_matrix

    def setup(self):
        # get all PyNodes of the transforms
        hier_a_matrix = get_hier_transformation(self.a)
        hier_b_matrix = get_hier_transformation(self.b)

        temp_matrix = self.a.getTransformation() * hier_a_matrix * hier_b_matrix.asMatrixInverse()
        self.relative_matrix = temp_matrix * self.b.getTransformation().asMatrixInverse()
        return self.relative_matrix

    def a_to_b(self):
        new_hier_a_matrix = get_hier_transformation(self.a)
        new_hier_b_matrix = get_hier_transformation(self.b)
        self.a.setMatrix(self.relative_matrix * self.b.getTransformation() * new_hier_b_matrix * new_hier_a_matrix.asMatrixInverse())

    def b_to_a(self):
        new_hier_a_matrix = get_hier_transformation(self.a)
        new_hier_b_matrix = get_hier_transformation(self.b)
        self.b.setMatrix(self.relative_matrix.asMatrixInverse() * self.a.getTransformation() * new_hier_a_matrix * new_hier_b_matrix.asMatrixInverse())
# ******************************************************************************************************************************************************


# 1. ********* UI с пресетами + функция стандартного сетапа **************
def get_selected_attribute():
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    attrs = pm.channelBox(channelBox, q=True, sma=True)
    if not attrs:
        return ""
    return attrs[0]


# validator class for coloring wrong values
class MyValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        super(MyValidator, self).__init__()
        self.parent = parent

    def validate(self, input_str, pos):
        if input_str == "":
            self.parent.setStyleSheet("background: palette(base);")
            return self.Acceptable
        elif pm.objExists(input_str):
            self.parent.setStyleSheet("background: darkgreen;")
            return self.Acceptable
        else:
            self.parent.setStyleSheet("background: darkred;")
            return self.Intermediate


# pick items widget
class PickWidget(QtWidgets.QWidget):
    def __init__(self, text, is_attribute=False):
        super(PickWidget, self).__init__()
        self.is_attribute = is_attribute
        self.lt = QtWidgets.QHBoxLayout(self)
        self.lt.setSpacing(10)
        self.lt.setMargin(0)
        self.label = QtWidgets.QLabel(text)
        self.label.setFixedWidth(150)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.line = QtWidgets.QLineEdit()
        self.validator = MyValidator(parent=self.line)
        self.line.setValidator(self.validator)
        self.button = QtWidgets.QPushButton("<<")
        self.button.clicked.connect(self.button_clicked)
        self.lt.addWidget(self.label)
        self.lt.addWidget(self.line)
        self.lt.addWidget(self.button)

    def button_clicked(self):
        lst = pm.ls(sl=True)
        if not lst:
            pm.warning("Select object")
            return
        if self.is_attribute:
            attr = get_selected_attribute()
            if not attr:
                pm.warning("Select attribute")
                return
            self.line.setText(lst[0].name() + "." + attr)
        else:
            self.line.setText(lst[0].name())


# UI for setup
class UIWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UIWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("IKFK Setup Window")
        self.setMinimumWidth(500)

        self.mb = QtWidgets.QMenuBar()
        self.presets_menu = QtWidgets.QMenu("Presets")
        self.mb.addMenu(self.presets_menu)

        self.menu_action_right_hand = QtWidgets.QAction("Right Hand", self)
        self.menu_action_right_hand.triggered.connect(self.action_right_hand_clicked)
        self.presets_menu.addAction(self.menu_action_right_hand)
        self.menu_action_left_hand = QtWidgets.QAction("Left Hand", self)
        self.menu_action_left_hand.triggered.connect(self.action_left_hand_clicked)
        self.presets_menu.addAction(self.menu_action_left_hand)
        self.menu_action_right_leg = QtWidgets.QAction("Right Leg", self)
        self.menu_action_right_leg.triggered.connect(self.action_right_leg_clicked)
        self.presets_menu.addAction(self.menu_action_right_leg)
        self.menu_action_left_leg = QtWidgets.QAction("Left Leg", self)
        self.menu_action_left_leg.triggered.connect(self.action_left_leg_clicked)
        self.presets_menu.addAction(self.menu_action_left_leg)
        self.menu_clear = QtWidgets.QAction("Clear", self)
        self.menu_clear.triggered.connect(self.action_clear_clicked)
        self.presets_menu.addAction(self.menu_clear)

        spacer_height = 10
        self.vert_lo = QtWidgets.QVBoxLayout(self)
        self.vert_lo.setMenuBar(self.mb)
        self.vert_lo.setSpacing(5)
        self.vert_lo.setMargin(10)
        self.vert_lo.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.pw_main = PickWidget("Config Node: ")
        self.vert_lo.addWidget(self.pw_main)
        self.vert_lo.addSpacing(spacer_height)
        self.pw_ik_wrist = PickWidget("Wrist (C) IK: ")
        self.vert_lo.addWidget(self.pw_ik_wrist)
        self.pw_ik_pole = PickWidget("PoleVector IK: ")
        self.vert_lo.addWidget(self.pw_ik_pole)
        self.pw_ik_dop = PickWidget("Dop IK: ")
        self.vert_lo.addWidget(self.pw_ik_dop)
        self.vert_lo.addSpacing(spacer_height)
        self.pw_fk_shoulder = PickWidget("Shoulder (A) FK: ")
        self.vert_lo.addWidget(self.pw_fk_shoulder)
        self.pw_fk_elbow = PickWidget("Elbow (B) FK: ")
        self.vert_lo.addWidget(self.pw_fk_elbow)
        self.pw_fk_wrist = PickWidget("Wrist (C) FK: ")
        self.vert_lo.addWidget(self.pw_fk_wrist)
        self.vert_lo.addSpacing(spacer_height)
        self.pw_sk_shoulder = PickWidget("Shoulder (A) JNT: ")
        self.vert_lo.addWidget(self.pw_sk_shoulder)
        self.pw_sk_elbow = PickWidget("Elbow (B) JNT: ")
        self.vert_lo.addWidget(self.pw_sk_elbow)
        self.pw_sk_wrist = PickWidget("Wrist (C) JNT: ")
        self.vert_lo.addWidget(self.pw_sk_wrist)
        self.vert_lo.addSpacing(spacer_height)
        self.pw_fk_ik_blend_attr = PickWidget("FK-IK Blend ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_fk_ik_blend_attr)
        self.hor_lo = QtWidgets.QHBoxLayout()
        self.hor_lo.setAlignment(QtCore.Qt.AlignRight)
        label = QtWidgets.QLabel("Invert FK-IK")
        self.hor_lo.addWidget(label)
        self.ikfk_switch_widget = QtWidgets.QCheckBox("         ")
        self.hor_lo.addWidget(self.ikfk_switch_widget)
        self.vert_lo.addLayout(self.hor_lo)
        self.pw_ik_lower_length = PickWidget("Lower Length IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_ik_lower_length)
        self.pw_ik_upper_length = PickWidget("Upper Length IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_ik_upper_length)
        self.pw_ik_double_length = PickWidget("Double Length IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_ik_double_length)
        self.pw_softness_attr = PickWidget("Softness IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_softness_attr)
        self.pw_roll_attr = PickWidget("Roll IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_roll_attr)
        self.pw_rock_attr = PickWidget("Rock IK ATTR: ", is_attribute=True)
        self.vert_lo.addWidget(self.pw_rock_attr)
        self.vert_lo.addSpacing(spacer_height)
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setFixedWidth(100)
        self.save_button.clicked.connect(self.on_save_clicked)
        self.vert_lo.addWidget(self.save_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

    def on_save_clicked(self):
        setup_save(self.pw_main.line.text(), self.pw_ik_wrist.line.text(), self.pw_ik_pole.line.text(),
                   self.pw_ik_dop.line.text(), self.pw_fk_shoulder.line.text(), self.pw_fk_elbow.line.text(),
                   self.pw_fk_wrist.line.text(), self.pw_sk_shoulder.line.text(), self.pw_sk_elbow.line.text(), self.pw_sk_wrist.line.text(),
                   self.pw_fk_ik_blend_attr.line.text(), self.pw_ik_lower_length.line.text(), self.pw_ik_upper_length.line.text(), self.pw_ik_double_length.line.text(),
                   self.pw_softness_attr.line.text(), self.pw_roll_attr.line.text(), self.pw_rock_attr.line.text(), self.ikfk_switch_widget.isChecked())
        self.action_clear_clicked()

    def action_right_hand_clicked(self):
        self.pw_main.line.setText("Rt_Hand_CON")
        self.pw_ik_wrist.line.setText("Rt_IKArm_CON")
        self.pw_ik_pole.line.setText("Rt_PoleHand_CON")
        self.pw_ik_dop.line.setText("")
        self.pw_fk_shoulder.line.setText("Rt_Shoulder_CON")
        self.pw_fk_elbow.line.setText("Rt_Elbow_CON")
        self.pw_fk_wrist.line.setText("Rt_Wrist_CON")
        self.pw_sk_shoulder.line.setText("Rt_Arm_01_JNT")
        self.pw_sk_elbow.line.setText("Rt_Arm_02_JNT")
        self.pw_sk_wrist.line.setText("Rt_Arm_03_JNT")
        self.pw_fk_ik_blend_attr.line.setText("Rt_Hand_CON.FK_IK_blend")
        self.pw_ik_lower_length.line.setText("Rt_Hand_CON.IK_LowerLength")
        self.pw_ik_upper_length.line.setText("Rt_Hand_CON.IK_UpperLength")
        self.pw_ik_double_length.line.setText("Rt_Hand_CON.IK_LengthDouble")
        self.pw_softness_attr.line.setText("Rt_Hand_CON.IKSoftness")
        self.pw_roll_attr.line.setText("")
        self.pw_rock_attr.line.setText("")

    def action_left_hand_clicked(self):
        self.pw_main.line.setText("Lf_Hand_CON")
        self.pw_ik_wrist.line.setText("Lf_IKArm_CON")
        self.pw_ik_pole.line.setText("Lf_PoleHand_CON")
        self.pw_ik_dop.line.setText("")
        self.pw_fk_shoulder.line.setText("Lf_Shoulder_CON")
        self.pw_fk_elbow.line.setText("Lf_Elbow_CON")
        self.pw_fk_wrist.line.setText("Lf_Wrist_CON")
        self.pw_sk_shoulder.line.setText("Lf_Arm_01_JNT")
        self.pw_sk_elbow.line.setText("Lf_Arm_02_JNT")
        self.pw_sk_wrist.line.setText("Lf_Arm_03_JNT")
        self.pw_fk_ik_blend_attr.line.setText("Lf_Hand_CON.FK_IK_blend")
        self.pw_ik_lower_length.line.setText("Lf_Hand_CON.IK_LowerLength")
        self.pw_ik_upper_length.line.setText("Lf_Hand_CON.IK_UpperLength")
        self.pw_ik_double_length.line.setText("Lf_Hand_CON.IK_LengthDouble")
        self.pw_softness_attr.line.setText("Lf_Hand_CON.IKSoftness")
        self.pw_roll_attr.line.setText("")
        self.pw_rock_attr.line.setText("")

    def action_right_leg_clicked(self):
        self.pw_main.line.setText("Rt_Leg_CON")
        self.pw_ik_wrist.line.setText("Rt_IKLeg_CON")
        self.pw_ik_pole.line.setText("Rt_PoleLeg_CON")
        self.pw_ik_dop.line.setText("Rt_IKLeg_Offset_CON")
        self.pw_fk_shoulder.line.setText("Rt_Hip_CON")
        self.pw_fk_elbow.line.setText("Rt_Knee_CON")
        self.pw_fk_wrist.line.setText("Rt_Ankle_CON")
        self.pw_sk_shoulder.line.setText("Rt_Leg_01_JNT")
        self.pw_sk_elbow.line.setText("Rt_Leg_02_JNT")
        self.pw_sk_wrist.line.setText("Rt_Leg_03_JNT")
        self.pw_fk_ik_blend_attr.line.setText("Rt_Leg_CON.FK_IK_blend")
        self.pw_ik_lower_length.line.setText("Rt_Leg_CON.IK_LowerLength")
        self.pw_ik_upper_length.line.setText("Rt_Leg_CON.IK_UpperLength")
        self.pw_ik_double_length.line.setText("Rt_Leg_CON.IK_LengthDouble")
        self.pw_softness_attr.line.setText("Rt_Leg_CON.IKSoftness")
        self.pw_roll_attr.line.setText("Rt_Leg_CON.IK_Foot_Roll")
        self.pw_rock_attr.line.setText("Rt_Leg_CON.IK_Side_Roll")

    def action_left_leg_clicked(self):
        self.pw_main.line.setText("Lf_Leg_CON")
        self.pw_ik_wrist.line.setText("Lf_IKLeg_CON")
        self.pw_ik_pole.line.setText("Lf_PoleLeg_CON")
        self.pw_ik_dop.line.setText("Lf_IKLeg_Offset_CON")
        self.pw_fk_shoulder.line.setText("Lf_Hip_CON")
        self.pw_fk_elbow.line.setText("Lf_Knee_CON")
        self.pw_fk_wrist.line.setText("Lf_Ankle_CON")
        self.pw_sk_shoulder.line.setText("Lf_Leg_01_JNT")
        self.pw_sk_elbow.line.setText("Lf_Leg_02_JNT")
        self.pw_sk_wrist.line.setText("Lf_Leg_03_JNT")
        self.pw_fk_ik_blend_attr.line.setText("Lf_Leg_CON.FK_IK_blend")
        self.pw_ik_lower_length.line.setText("Lf_Leg_CON.IK_LowerLength")
        self.pw_ik_upper_length.line.setText("Lf_Leg_CON.IK_UpperLength")
        self.pw_ik_double_length.line.setText("Lf_Leg_CON.IK_LengthDouble")
        self.pw_softness_attr.line.setText("Lf_Leg_CON.IKSoftness")
        self.pw_roll_attr.line.setText("Lf_Leg_CON.IK_Foot_Roll")
        self.pw_rock_attr.line.setText("Lf_Leg_CON.IK_Side_Roll")

    def action_clear_clicked(self):
        self.pw_main.line.setText("")
        self.pw_ik_wrist.line.setText("")
        self.pw_ik_pole.line.setText("")
        self.pw_ik_dop.line.setText("")
        self.pw_fk_shoulder.line.setText("")
        self.pw_fk_elbow.line.setText("")
        self.pw_fk_wrist.line.setText("")
        self.pw_sk_shoulder.line.setText("")
        self.pw_sk_elbow.line.setText("")
        self.pw_sk_wrist.line.setText("")
        self.pw_fk_ik_blend_attr.line.setText("")
        self.pw_ik_lower_length.line.setText("")
        self.pw_ik_upper_length.line.setText("")
        self.pw_ik_double_length.line.setText("")
        self.pw_softness_attr.line.setText("")
        self.pw_roll_attr.line.setText("")
        self.pw_rock_attr.line.setText("")


def create_ui():
    global ikfk_setup_win
    q_maya_window = get_maya_window()
    ikfk_setup_win = UIWidget(parent=q_maya_window)
    ikfk_setup_win.show()
    return ikfk_setup_win
# ************************************************************************


def set_attr(node, attr_name, value):
    if not pm.objExists(node.name() + '.' + attr_name):
        node.addAttr(attr_name, dt='string')
    node.attr(attr_name).unlock()
    node.attr(attr_name).set(value)
    node.attr(attr_name).lock()


def serialize_matrix(m):
    temp_str = ''
    for i in range(4):
        for j in range(4):
            q = str(round(m[i][j], 10)) + ','
            if q == '-0.0,':
                temp_str += '0.0,'
            else:
                temp_str += q
    temp_str = temp_str[:-1]
    return temp_str


def deserialize_matrix(m_str):
    splitted = m_str.split(',')
    temp_lst = []
    for x in splitted:
        temp_lst.append(float(x))
    return pm.datatypes.TransformationMatrix(temp_lst)


# ********* функция сетапа ***********************************************
def setup_save(*args):
    if len(args) < 18:
        pm.warning("Can't setup IK-FK")
        return 0
    config = ik_wrist = ik_pole = ik_dop = fk_shoulder = fk_elbow = fk_wrist = sk_shoulder = sk_elbow = sk_wrist = blend_attr = lower_length_attr = upper_length_attr = double_length_attr = softness_attr = roll_attr = rock_attr = None
    invert_ikfk = False
    if pm.objExists(args[0]):
        config = pm.PyNode(args[0])
    if pm.objExists(args[1]):
        ik_wrist = pm.PyNode(args[1])
    if pm.objExists(args[2]):
        ik_pole = pm.PyNode(args[2])
    if pm.objExists(args[3]):
        ik_dop = pm.PyNode(args[3])
    if pm.objExists(args[4]):
        fk_shoulder = pm.PyNode(args[4])
    if pm.objExists(args[5]):
        fk_elbow = pm.PyNode(args[5])
    if pm.objExists(args[6]):
        fk_wrist = pm.PyNode(args[6])
    if pm.objExists(args[7]):
        sk_shoulder = pm.PyNode(args[7])
    if pm.objExists(args[8]):
        sk_elbow = pm.PyNode(args[8])
    if pm.objExists(args[9]):
        sk_wrist = pm.PyNode(args[9])
    if pm.objExists(args[10]):
        blend_attr = pm.PyNode(args[10])
    if pm.objExists(args[11]):
        lower_length_attr = pm.PyNode(args[11])
    if pm.objExists(args[12]):
        upper_length_attr = pm.PyNode(args[12])
    if pm.objExists(args[13]):
        double_length_attr = pm.PyNode(args[13])
    if pm.objExists(args[14]):
        softness_attr = pm.PyNode(args[14])
    if pm.objExists(args[15]):
        roll_attr = pm.PyNode(args[15])
    if pm.objExists(args[16]):
        rock_attr = pm.PyNode(args[16])
    if args[17]:
        invert_ikfk = args[17]

    if not config:
        pm.warning("config node is missing")
        return 0
    if not ik_wrist or not ik_pole or not sk_shoulder or not sk_elbow or not sk_wrist or not fk_shoulder or not fk_elbow or not fk_wrist:
        pm.warning("one of the necessary nodes is missing")
        return 0

    # calc relative matrices of bones to FK controls
    sk_fk_shoulder_link = ObjLinker(sk_shoulder, fk_shoulder)
    sk_fk_shoulder_matrix = sk_fk_shoulder_link.setup()
    sk_fk_elbow_link = ObjLinker(sk_elbow, fk_elbow)
    sk_fk_elbow_matrix = sk_fk_elbow_link.setup()
    sk_fk_wrist_link = ObjLinker(sk_wrist, fk_wrist)
    sk_fk_wrist_matrix = sk_fk_wrist_link.setup()

    # calc relative matrix of fk relative to ik wrist
    fk_ik_wrist_link = ObjLinker(fk_wrist, ik_wrist)
    fk_ik_wrist_matrix = fk_ik_wrist_link.setup()

    # calc relative matrix of fk_elbow to ik_pole_vector. Needed only for straight hand(leg)
    fk_elbow_ik_pole_link = ObjLinker(fk_elbow, ik_pole)
    fk_elbow_ik_pole_matrix = fk_elbow_ik_pole_link.setup()

    # calc shoulder and elbow lengths
    shoulder_length = (sk_shoulder.getTranslation(space='world') - sk_elbow.getTranslation(space='world')).length()
    elbow_length = (sk_elbow.getTranslation(space='world') - sk_wrist.getTranslation(space='world')).length()

    temp_str = ''
    temp_str += ik_wrist.name() + ';' + ik_pole.name() + ';'
    if ik_dop:
        temp_str += ik_dop.name() + ';'
    else:
        temp_str += ";"
    temp_str += fk_shoulder.name() + ';' + fk_elbow.name() + ';' + fk_wrist.name() + ';'
    temp_str += sk_shoulder.name() + ';' + sk_elbow.name() + ';' + sk_wrist.name() + ';'
    if not blend_attr:
        pm.warning("blend_attr is missing")
        return 0
    temp_str += blend_attr.name() + ';' + str(blend_attr.getMin()) + ';' + str(blend_attr.getMax()) + ';'
    if lower_length_attr and upper_length_attr:
        temp_str += lower_length_attr.name() + ';' + str(lower_length_attr.get()) + ';' + upper_length_attr.name() + ';' + str(upper_length_attr.get()) + ';'
    else:
        temp_str += ";;;;"
    if double_length_attr:
        temp_str += double_length_attr.name() + ';' + str(double_length_attr.get()) + ';'
    else:
        temp_str += ";;"
    temp_str += str(shoulder_length) + ';' + str(elbow_length) + ';'
    if softness_attr:
        temp_str += softness_attr.name() + ';' + str(softness_attr.get()) + ';'
    else:
        temp_str += ';;'
    if roll_attr:
        temp_str += roll_attr.name() + ';' + str(roll_attr.get()) + ';'
    else:
        temp_str += ';;'
    if rock_attr:
        temp_str += rock_attr.name() + ';' + str(rock_attr.get()) + ';'
    else:
        temp_str += ';;'
    temp_str += str(invert_ikfk) + ';'
    temp_str += serialize_matrix(sk_fk_shoulder_matrix) + ';' + serialize_matrix(sk_fk_elbow_matrix) + ';' + serialize_matrix(sk_fk_wrist_matrix) + ';'
    temp_str += serialize_matrix(fk_ik_wrist_matrix) + ';'
    temp_str += serialize_matrix(fk_elbow_ik_pole_matrix) + ';'

    set_attr(config, 'ikfk_setup', temp_str)
    set_attr(config, 'ikfk_config_node', config.name())
    set_attr(ik_wrist, 'ikfk_config_node', config.name())
    set_attr(ik_pole, 'ikfk_config_node', config.name())
    if ik_dop:
        set_attr(ik_dop, 'ikfk_config_node', config.name())
    set_attr(fk_shoulder, 'ikfk_config_node', config.name())
    set_attr(fk_elbow, 'ikfk_config_node', config.name())
    set_attr(fk_wrist, 'ikfk_config_node', config.name())
    return 1


class IKFK():
    def __init__(self):
        self.config = None
        self.con = None
        self.ik_lst = []
        self.fk_lst = []
        self.ik_wrist = self.ik_pole = self.ik_dop = None
        self.fk_shoulder = self.fk_elbow = self.fk_wrist = None
        self.sk_shoulder = self.sk_elbow = self.sk_wrist = None
        self.blend_attr = None
        self.blend_attr_min = self.blend_attr_max = -1
        self.lower_length_attr = self.upper_length_attr = self.double_length_attr = None
        self.lower_length_attr_val = self.upper_length_attr_val = self.double_length_attr_val = -1
        self.shoulder_length = self.elbow_length = -1
        self.softness_attr = self.roll_attr = self.rock_attr = None
        self.softness_attr_val = self.roll_attr_val = self.rock_attr_val = -1
        self.invert_ikfk = False
        self.sk_fk_shoulder_matrix = self.sk_fk_elbow_matrix = self.sk_fk_wrist_matrix = None
        self.fk_ik_wrist_matrix = None
        self.fk_elbow_ik_pole_matrix = None
        self.setup_load()

    def setup_load(self):
        lst = pm.ls(sl=True)
        if not lst:
            pm.warning("select control")
            return
        self.con = lst[0]
        if not pm.objExists(self.con + ".ikfk_config_node"):
            pm.warning("control is not set up")
            return
        ns = self.con.namespace()
        self.config = pm.PyNode(ns + self.con.ikfk_config_node.get())
        if not pm.objExists(self.config + ".ikfk_setup"):
            pm.warning("config node is not set up")
            return
        config_str = self.config.ikfk_setup.get()
        splitted = config_str.split(';')
        self.ik_lst = []
        self.fk_lst = []
        if splitted[0]:
            self.ik_wrist = pm.PyNode(ns + splitted[0])
            self.ik_lst.append(splitted[0])
        if splitted[1]:
            self.ik_pole = pm.PyNode(ns + splitted[1])
            self.ik_lst.append(splitted[1])

        if splitted[2]:
            self.ik_dop = pm.PyNode(ns + splitted[2])
            self.ik_lst.append(splitted[2])

        if splitted[3]:
            self.fk_shoulder = pm.PyNode(ns + splitted[3])
            self.fk_lst.append(splitted[3])
        if splitted[4]:
            self.fk_elbow = pm.PyNode(ns + splitted[4])
            self.fk_lst.append(splitted[4])
        if splitted[5]:
            self.fk_wrist = pm.PyNode(ns + splitted[5])
            self.fk_lst.append(splitted[5])
        if splitted[6]:
            self.sk_shoulder = pm.PyNode(ns + splitted[6])
        if splitted[7]:
            self.sk_elbow = pm.PyNode(ns + splitted[7])
        if splitted[8]:
            self.sk_wrist = pm.PyNode(ns + splitted[8])
        if splitted[9]:
            self.blend_attr = pm.PyNode(ns + splitted[9])
        if splitted[10]:
            self.blend_attr_min = float(splitted[10])
        if splitted[11]:
            self.blend_attr_max = float(splitted[11])
        if splitted[12]:
            self.lower_length_attr = pm.PyNode(ns + splitted[12])
        if splitted[13]:
            self.lower_length_attr_val = float(splitted[13])
        if splitted[14]:
            self.upper_length_attr = pm.PyNode(ns + splitted[14])
        if splitted[15]:
            self.upper_length_attr_val = float(splitted[15])
        if splitted[16]:
            self.double_length_attr = pm.PyNode(ns + splitted[16])
        if splitted[17]:
            self.double_length_attr_val = float(splitted[17])
        if splitted[18]:
            self.shoulder_length = float(splitted[18])
        if splitted[19]:
            self.elbow_length = float(splitted[19])
        if splitted[20]:
            self.softness_attr = pm.PyNode(ns + splitted[20])
        if splitted[21]:
            self.softness_attr_val = float(splitted[21])
        if splitted[22]:
            self.roll_attr = pm.PyNode(ns + splitted[22])
        if splitted[23]:
            self.roll_attr_val = float(splitted[23])
        if splitted[24]:
            self.rock_attr = pm.PyNode(ns + splitted[24])
        if splitted[25]:
            self.rock_attr_val = float(splitted[25])
        if splitted[26]:
            self.invert_ikfk = eval(splitted[26])
        if splitted[27]:
            self.sk_fk_shoulder_matrix = deserialize_matrix(splitted[27])
        if splitted[28]:
            self.sk_fk_elbow_matrix = deserialize_matrix(splitted[28])
        if splitted[29]:
            self.sk_fk_wrist_matrix = deserialize_matrix(splitted[29])
        if splitted[30]:
            self.fk_ik_wrist_matrix = deserialize_matrix(splitted[30])
        if splitted[31]:
            self.fk_elbow_ik_pole_matrix = deserialize_matrix(splitted[31])

    def ik_to_fk(self):
        linker_shoulder = ObjLinker(self.sk_shoulder, self.fk_shoulder, self.sk_fk_shoulder_matrix)
        linker_shoulder.b_to_a()
        linker_elbow = ObjLinker(self.sk_elbow, self.fk_elbow, self.sk_fk_elbow_matrix)
        linker_elbow.b_to_a()
        linker_wrist = ObjLinker(self.sk_wrist, self.fk_wrist, self.sk_fk_wrist_matrix)
        linker_wrist.b_to_a()

        if not self.invert_ikfk:
            self.blend_attr.set(self.blend_attr_min)
        else:
            self.blend_attr.set(self.blend_attr_max)

    def fk_to_ik(self):
        # flush some of ik attrs to default vals
        if self.softness_attr and self.softness_attr_val != -1:
            self.softness_attr.set(self.softness_attr_val)
        if self.roll_attr and self.roll_attr_val != -1:
            self.roll_attr.set(self.roll_attr_val)
        if self.rock_attr and self.rock_attr_val != -1:
            self.rock_attr.set(self.rock_attr_val)
        if self.double_length_attr and self.double_length_attr_val != -1:
            self.double_length_attr.set(self.double_length_attr_val)

        # calculate stretching attrs
        if self.lower_length_attr and self.upper_length_attr and self.elbow_length and self.shoulder_length and self.lower_length_attr_val != -1 and self.upper_length_attr_val != -1:
            current_shoulder_length = (self.sk_shoulder.getTranslation(space='world') - self.sk_elbow.getTranslation(space='world')).length()
            current_elbow_length = (self.sk_elbow.getTranslation(space='world') - self.sk_wrist.getTranslation(space='world')).length()
            if round(current_elbow_length, 10) != round(self.elbow_length, 10):
                k = current_elbow_length / self.elbow_length
                new_value = self.lower_length_attr_val * k
                if new_value <= self.lower_length_attr.getMax():
                    self.lower_length_attr.set(new_value)
                else:
                    pm.warning("Can't set lower_length above maximum value")
                    self.lower_length_attr.set(self.lower_length_attr.getMax())
            if round(current_shoulder_length, 10) != round(self.shoulder_length, 10):
                k = current_shoulder_length / self.shoulder_length
                new_value = self.upper_length_attr_val * k
                if new_value <= self.upper_length_attr.getMax():
                    self.upper_length_attr.set(new_value)
                else:
                    pm.warning("Can't set upper_length above maximum value")
                    self.upper_length_attr.set(self.upper_length_attr.getMax())

        # set ik_wrist to fk_wrist
        linker_wrist = ObjLinker(self.fk_wrist, self.ik_wrist, self.fk_ik_wrist_matrix)
        linker_wrist.b_to_a()

        # set pole-vector
        linker_elb = ObjLinker(self.fk_elbow, self.ik_pole, self.fk_elbow_ik_pole_matrix)
        linker_elb.b_to_a()

        # set dop control to default
        if self.ik_dop:
            self.ik_dop.setTranslation([0, 0, 0])
            self.ik_dop.setRotation([0, 0, 0])

        # switch blend attr
        if not self.invert_ikfk:
            self.blend_attr.set(self.blend_attr_max)
        else:
            self.blend_attr.set(self.blend_attr_min)

    def switcher(self):
        if not self.con or not self.ik_lst or not self.fk_lst:
            return
        if self.con.name(stripNamespace=True) in self.ik_lst:
            self.ik_to_fk()
            pm.select(self.fk_wrist)
        elif self.con.name(stripNamespace=True) in self.fk_lst:
            self.fk_to_ik()
            pm.select(self.ik_wrist)
        elif self.con == self.config:
            if not self.invert_ikfk:
                if self.blend_attr.get() == self.blend_attr_max:
                    self.ik_to_fk()
                    pm.select(self.fk_wrist)
                else:
                    self.fk_to_ik()
                    pm.select(self.ik_wrist)
            else:
                if self.blend_attr.get() == self.blend_attr_min:
                    self.ik_to_fk()
                    pm.select(self.fk_wrist)
                else:
                    self.fk_to_ik()
                    pm.select(self.ik_wrist)

# ************************************************************************
