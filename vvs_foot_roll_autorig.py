import pymel.core as pm
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import os
import shiboken2.wrapInstance as wrp
import maya.OpenMayaUI as omui

# module to make tricky spline footroll

# to run - call create_ui()
# place an imported curve according to right leg
# push Symmetry Rt->Lf
# push bind button
# P.S. - All node names are hadcoded. Please check and tune script. Works fine with advanced skeleton rigs

foot_tool_win = None


# gettin maya window
def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrp(long(ptr), QtWidgets.QMainWindow)


def get_script_folder():
    return os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]


class FootRoll_UI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FootRoll_UI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Add Foot Roll Tool")
        self.setMinimumWidth(400)
        self.vert_lo = QtWidgets.QVBoxLayout(self)
        self.button1 = QtWidgets.QPushButton("Import Setup")
        self.button1.clicked.connect(self.import_setup)
        self.vert_lo.addWidget(self.button1)
        self.button2 = QtWidgets.QPushButton("Symmetry Rt -> Lf")
        self.button2.clicked.connect(self.mirror)
        self.vert_lo.addWidget(self.button2)
        self.button3 = QtWidgets.QPushButton("Bind")
        self.button3.clicked.connect(self.bind)
        self.vert_lo.addWidget(self.button3)

    def import_setup(self):
        # 1
        pm.system.importFile(get_script_folder() + "/footRoll_setup.ma")
        self.curve_r = pm.PyNode('Rt_FootRollLimitCrv')
        self.curve_l = pm.PyNode('Lf_FootRollLimitCrv')
        self.curve_r_shape = self.curve_r.getShape()
        self.curve_l_shape = self.curve_l.getShape()
        self.curve_r.setParent(None)
        self.curve_l.setParent(None)
        self.ik_control_r = pm.PyNode('IKLeg_R')
        self.ik_control_l = pm.PyNode('IKLeg_L')
        self.curve_r.setTranslation(self.ik_control_r.getTranslation(space='world'), space='world')
        self.curve_r.setRotation(self.ik_control_r.getRotation(space='world'), space='world')
        self.curve_l.setTranslation(self.ik_control_l.getTranslation(space='world'), space='world')
        self.curve_l.setRotation(self.ik_control_l.getRotation(space='world'), space='world')
        cvs_r = self.curve_r_shape.getCVs(space='world')
        cvs_l = self.curve_l_shape.getCVs(space='world')
        for i in range(len(cvs_r)):
            cvs_r[i][1] = 0.0
            cvs_l[i][1] = 0.0
        self.curve_r_shape.setCVs(cvs_r, space='world')
        self.curve_l_shape.setCVs(cvs_l, space='world')
        self.curve_r_shape.updateCurve()
        self.curve_l_shape.updateCurve()
        pm.select(self.curve_r)
        # pm.selectType(allObjects=True, allComponents=False, cv=True)
        # pm.selectMode(component=True)

    def mirror(self):
        cvs = self.curve_r_shape.getCVs(space='world')
        new_positions = []
        for cv in cvs:
            new_positions.append(pm.datatypes.Point(-cv[0], cv[1], cv[2]))
        self.curve_l_shape.setCVs(new_positions, space='world')
        self.curve_l_shape.updateCurve()

    def process(self, prefix, suffix):
        # 4
        self.ik_control = pm.PyNode("IKLeg" + suffix)
        self.curve = pm.PyNode(prefix + "FootRollLimitCrv")
        self.ik_align = pm.PyNode(prefix + "IKLeg_align")
        self.ik_align.setTranslation(self.ik_control.getTranslation(space='world'), space='world')
        self.ik_align.setRotation(self.ik_control.getRotation(space='world'), space='world')
        self.ik_align.setParent(self.ik_control)
        self.curve.setParent(self.ik_align)
        self.curve.overrideEnabled.set(1)
        self.curve.overrideDisplayType.set(2)

        # 5
        toes_joint = pm.PyNode("Toes" + suffix)
        ikroll_toes_grp = pm.PyNode(prefix + "IKRollToes_GRP")
        ik_toes_grp = pm.PyNode(prefix + "IKToes_GRP")
        ikroll_toes_grp.setTranslation(toes_joint.getTranslation(space="world"), space="world")
        ik_toes_grp.setTranslation(toes_joint.getTranslation(space="world"), space="world")

        # 6
        pm.select(d=True)
        jnt1 = pm.joint(n=prefix + "IK_Ankle")
        jnt2 = pm.joint(n=prefix + "IK_Toes")
        jnt3 = pm.joint(n=prefix + "IK_ToesEnd")

        ankle = pm.PyNode("Ankle" + suffix)
        toes = pm.PyNode("Toes" + suffix)
        toes_end = pm.PyNode("ToesEnd" + suffix)

        jnt1.setTranslation(ankle.getTranslation(space="world"), space="world")
        jnt1.setRotation(ankle.getRotation(space="world"), space="world")
        jnt2.setTranslation(toes.getTranslation(space="world"), space="world")
        jnt2.setRotation(toes.getRotation(space="world"), space="world")
        jnt3.setTranslation(toes_end.getTranslation(space="world"), space="world")
        jnt3.setRotation(toes_end.getRotation(space="world"), space="world")

        pm.makeIdentity(jnt1, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt2, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt3, apply=True, t=True, r=True, s=True, n=False, pn=True)

        ikxknee = pm.PyNode("IKXKnee" + suffix)
        jnt1.setParent(ikxknee)

        # 7
        pm.select(d=True)
        jnt4 = pm.joint(n=prefix + "RevHeel")
        roll_heel = pm.PyNode("RollHeel" + suffix)
        jnt4.setTranslation(roll_heel.getTranslation(space="world"), space="world")
        jnt4.setRotation(self.ik_control.getRotation(space="world"), space="world")
        jnt1 = pm.duplicate(jnt4, n=prefix + "FootRollMain")[0]
        jnt1.setParent(None)
        jnt2 = pm.duplicate(jnt4, n=prefix + "FootRollPivot")[0]
        jnt2.setParent(jnt1)
        jnt3 = pm.duplicate(jnt4, n=prefix + "FootReCenter")[0]
        jnt3.setParent(jnt2)
        jnt4.setParent(jnt3)
        pm.select(jnt4)
        jnt5 = pm.joint(n=prefix + "RevToeEnd")
        roll_toes = pm.PyNode("RollToesEnd" + suffix)
        jnt5.setTranslation(roll_toes.getTranslation(space="world"), space="world")
        jnt5.setRotation(self.ik_control.getRotation(space="world"), space="world")
        jnt6 = pm.joint(n=prefix + "RevToe")
        jnt6.setTranslation(toes.getTranslation(space="world"), space="world")
        jnt6.setRotation(self.ik_control.getRotation(space="world"), space="world")
        jnt7 = pm.joint(n=prefix + "RevAnkle")
        jnt7.setTranslation(ankle.getTranslation(space="world"), space="world")
        jnt7.setRotation(self.ik_control.getRotation(space="world"), space="world")
        pm.makeIdentity(jnt1, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt2, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt3, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt4, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt5, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt6, apply=True, t=True, r=True, s=True, n=False, pn=True)
        pm.makeIdentity(jnt7, apply=True, t=True, r=True, s=True, n=False, pn=True)
        jnt1.setParent(prefix + "IKLeg_align")

        # 8
        mult_div = pm.createNode("multiplyDivide", n="mult" + suffix)
        mult_div.operation.set(1)
        mult_div.input2.set([-1, -1, -1])
        jnt2.translate.connect(mult_div.input1)
        mult_div.output.connect(jnt3.translate)

        # 9
        curve_info_roll = pm.PyNode(prefix + "pointOnCurveInfo_Roll")
        roll_limit_shape = pm.PyNode(prefix + "FootRollLimitCrvShape")
        roll_limit_shape.ws[0].connect(curve_info_roll.inputCurve)

        # 10
        pm.pointConstraint(prefix + "footRollLimitLoc", jnt2, mo=False, n="footroll_PC_loc" + suffix)
        ik_roll_con = pm.PyNode(prefix + "IKFootRoll_CON")
        ik_roll_con.rotateX.connect(jnt2.rotateX)
        ik_roll_con.rotate_pivot.connect(jnt2.rotateY)
        ik_roll_con.rotateZ.connect(jnt2.rotateZ)

        # 11
        roll_toes_GRP = pm.PyNode(prefix + "IKRollToes_GRP")
        ik_toes_GRP = pm.PyNode(prefix + "IKToes_GRP")
        roll_toes_GRP.setParent(prefix + "RevToe")
        ik_toes_GRP.setParent(prefix + "RevToeEnd")

        # 12
        ball_ik_handle = pm.ikHandle(sj=prefix + "IK_Ankle", ee=prefix + "IK_Toes", sol="ikSCsolver", n=prefix + "ball_ikHandle")[0]
        ball_ik_handle.visibility.set(0)
        ball_ik_handle.setParent(prefix + "IKRollToes_CON")

        toe_ik_handle = pm.ikHandle(sj=prefix + "IK_Toes", ee=prefix + "IK_ToesEnd", sol="ikSCsolver", n=prefix + "toe_ikHandle")[0]
        toe_ik_handle.visibility.set(0)
        toe_ik_handle.setParent(prefix + "IKToes_CON")

        # 13
        remap_value_toe = pm.PyNode(prefix + "remapValue_Toe")
        rev_toe = pm.PyNode(prefix + "RevToe")
        remap_value_toe_end = pm.PyNode(prefix + "remapValue_ToeEnd")
        rev_toe_end = pm.PyNode(prefix + "RevToeEnd")
        remap_value_toe.outValue.connect(rev_toe.rotateX)
        remap_value_toe_end.outValue.connect(rev_toe_end.rotateX)

        # 14
        pole_lock = pm.PyNode("PoleLockBlenderIKXAnkle" + suffix)
        ik_ankle = pm.PyNode(prefix + "IK_Ankle")
        pole_lock.output.connect(ik_ankle.translateX)

        # 15
        self.ik_control.addAttr("new_footRoll", at="float", k=True, min=0.0, max=1.0)

        # 16
        ik_leg_handle_grp = pm.group(em=True, name="IKLegHandle" + suffix + "_GRP")
        ik_leg_handle_grp.setTranslation(self.ik_control.getTranslation(space="world"), space="world")
        ik_leg_handle_grp.setRotation(self.ik_control.getRotation(space="world"), space="world")
        ik_leg_handle_grp.setParent(self.ik_control)
        adv_ik_handler = pm.PyNode("IKLegHandle" + suffix)
        adv_ik_handler.setParent(ik_leg_handle_grp)

        # 17
        constr = pm.parentConstraint("RollToes" + suffix, prefix + "IKRollToes_CON", "IKLegHandle" + suffix + "_GRP", mo=True)
        constr.interpType.set(2)
        reverse_node = pm.createNode("reverse", n="reverse_IKLeg" + suffix)
        self.ik_control.new_footRoll.connect(reverse_node.inputX)
        reverse_node.outputX.connect(constr.attr("RollToes" + suffix + "W0"))
        self.ik_control.new_footRoll.connect(constr.attr(prefix + "IKRollToes_CONW1"))

        # 18
        point_constr = pm.pointConstraint(prefix + "IK_Toes", "Toes" + suffix, mo=True)
        orient_constr = pm.orientConstraint(prefix + "IK_Toes", "Toes" + suffix, mo=True)
        orient_constr.interpType.set(2)

        fk_ik_blend_leg_unit_conv = pm.PyNode("FKIKBlendLegUnitConversion" + suffix)

        new_reverse = pm.createNode("reverse", n=prefix + "rev_node")
        new_float_math1 = pm.createNode("floatMath", n=prefix + "floatMath_node1")
        new_float_math1.operation.set(2)
        new_float_math2 = pm.createNode("floatMath", n=prefix + "floatMath_node2")
        new_float_math2.operation.set(2)

        self.ik_control.new_footRoll.connect(new_float_math1.floatA)
        self.ik_control.new_footRoll.connect(new_reverse.inputX)
        new_reverse.outputX.connect(new_float_math2.floatA)
        new_float_math1.outFloat.connect(point_constr.attr(prefix + "IK_ToesW2"))
        new_float_math1.outFloat.connect(orient_constr.attr(prefix + "IK_ToesW2"))
        new_float_math2.outFloat.connect(point_constr.attr("IKXToes" + suffix + "W1"), f=True)
        new_float_math2.outFloat.connect(orient_constr.attr("IKXToes" + suffix + "W1"), f=True)
        fk_ik_blend_leg_unit_conv.output.connect(new_float_math1.floatB)
        fk_ik_blend_leg_unit_conv.output.connect(new_float_math2.floatB)

        # 19
        point_constr2 = pm.pointConstraint(prefix + "IK_Ankle", "FKIKMixAnkle" + suffix, mo=True)
        new_float_math3 = pm.createNode("floatMath", n="floatMath_reverse_IKLeg" + suffix)
        new_float_math3.operation.set(2)
        new_float_math4 = pm.createNode("floatMath", n="floatMath_IKLeg" + suffix)
        new_float_math4.operation.set(2)
        self.ik_control.new_footRoll.connect(new_float_math4.floatB)
        reverse_node.outputX.connect(new_float_math3.floatA)
        fk_ik_blend_leg_unit_conv.output.connect(new_float_math3.floatB)
        fk_ik_blend_leg_unit_conv.output.connect(new_float_math4.floatA)
        new_float_math3.outFloat.connect(point_constr2.attr("IKXAnkle" + suffix + "W1"), f=True)
        new_float_math4.outFloat.connect(point_constr2.attr(prefix + "IK_AnkleW2"), f=True)

        # 20
        pc_20 = pm.parentConstraint(prefix + "IK_Ankle", "BendKneeLocator4" + suffix, mo=True)
        pc_20.interpType.set(2)
        new_float_math4.outFloat.connect(pc_20.attr(prefix + "IK_AnkleW2"), f=True)
        new_float_math3.outFloat.connect(pc_20.attr("IKXAnkle" + suffix + "W1"), f=True)

        # 21
        pc_21 = pm.pointConstraint(prefix + "IK_Ankle", "Ankle" + suffix, mo=True)
        oc_21 = pm.orientConstraint(prefix + "IK_Ankle", "Ankle" + suffix, mo=True)
        oc_21.interpType.set(2)
        new_float_math4.outFloat.connect(pc_21.attr(prefix + "IK_AnkleW2"), f=True)
        new_float_math3.outFloat.connect(pc_21.attr("IKXAnkle" + suffix + "W1"), f=True)
        new_float_math4.outFloat.connect(oc_21.attr(prefix + "IK_AnkleW2"), f=True)
        new_float_math3.outFloat.connect(oc_21.attr("IKXAnkle" + suffix + "W1"), f=True)

        # 22
        pivot = pm.PyNode("IKLegFootRockInnerPivot" + suffix)
        new_float_math3.outFloat.connect(pivot.visibility, f=True)
        new_float_math4.outFloat.connect(self.ik_align.visibility, f=True)

    def bind(self):
        # pm.selectType(allObjects=True, allComponents=True)
        # pm.selectMode(object=True)
        self.process("Rt_", "_R")
        self.process("Lf_", "_L")


def create_ui():
    global curve_blendshape_tool_win
    q_maya_window = get_maya_window()
    foot_tool_win = FootRoll_UI(parent=q_maya_window)
    foot_tool_win.show()
