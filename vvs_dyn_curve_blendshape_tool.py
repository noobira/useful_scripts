import pymel.core as pm
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import collections
import maya.mel as mel
import shiboken2.wrapInstance as wrp
import maya.OpenMayaUI as omui


# this tool was made for hair dynamics. So it works on curves. It morphs group of curves to different blendshape targets, which you are creating.
# You need a curves in group. It's important.
# create_ui()
# push start edit button to start moving cvs
# end to finish with this frame


curve_blendshape_tool_win = None


# gettin maya window
def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrp(long(ptr), QtWidgets.QMainWindow)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Curves Blendshape Tool")
        self.setMinimumWidth(400)

        self.group = None
        self.blendshape = None
        self.base_shape = collections.OrderedDict()
        self.key_target_dict = {}
        self.idx = None
        self.new_key = False

        style_sheet = """
            QPushButton {{
                font: {0}px;
                height: {1}px;
                background-color: palette(Button);
                border-radius: {2}px;
                padding: {3}px {3}px {3}px {3}px;
            }}
            QPushButton:hover{{
                            background-color: #707070;
            }}
            QPushButton:pressed {{
                background-color: palette(Dark);
            }}
            QLineEdit {{
                font: {0}px;
                height: {1}px;
                background-color: #2b2b2b;
                border-radius: {2}px;
                padding: {3}px {3}px {3}px {3}px;
            }}""".format(16, 22, 5, 4)

        self.setStyleSheet(style_sheet)
        self.vert_lo0 = QtWidgets.QVBoxLayout(self)
        self.vert_lo0.setAlignment(QtCore.Qt.AlignTop)

        self.hor_lo0 = QtWidgets.QHBoxLayout()
        self.group_label = QtWidgets.QLineEdit()
        self.group_label.setDisabled(True)
        self.btn0 = QtWidgets.QPushButton("Get group")
        self.btn0.clicked.connect(self.get_group)
        self.btn0.setFixedWidth(100)
        self.hor_lo0.addWidget(self.group_label)
        self.hor_lo0.addWidget(self.btn0)
        self.hor_lo0.setContentsMargins(0, 3, 0, 3)

        self.hor_lo2 = QtWidgets.QHBoxLayout()
        self.btn6 = QtWidgets.QPushButton("Start Edit")
        self.btn6.clicked.connect(self.edit_clicked)
        self.btn7 = QtWidgets.QPushButton("End Edit")
        self.btn7.clicked.connect(self.end_clicked)
        self.btn8 = QtWidgets.QPushButton("Key base shape")
        self.btn8.clicked.connect(self.kbs_clicked)
        self.hor_lo2.addWidget(self.btn6)
        self.hor_lo2.addWidget(self.btn7)
        self.hor_lo2.setContentsMargins(0, 3, 0, 3)

        self.vert_lo0.addLayout(self.hor_lo0)
        self.vert_lo0.addWidget(self.btn8)
        self.vert_lo0.addLayout(self.hor_lo2)

    def get_existed_blendshape(self):
        if not self.group:
            return None
        children = self.group.getChildren()
        if not children:
            return None
        blendshapes = children[0].getShape().connections(type='blendShape')
        if not blendshapes:
            return None
        return blendshapes[0]

    def get_group(self):
        self.group = None
        self.blendshape = None
        self.base_shape = collections.OrderedDict()
        self.key_target_dict = {}
        self.new_key = False

        lst = pm.ls(sl=True)
        if not lst:
            pm.warning("Select curve or group")
            return
        if lst[0].type() == 'transform':
            if not lst[0].getShape():
                self.group = lst[0]
                self.group_label.setText(lst[0].name())
            elif lst[0].getShape().type() == 'nurbsCurve':
                supposed_group = pm.listRelatives(lst[0], p=True)
                if not supposed_group or supposed_group[0].getShape():
                    pm.warning("No group above")
                    return
                self.group = supposed_group[0]
                self.group_label.setText(supposed_group[0].name())
            else:
                pm.warning("Select curve or group")
                return
        elif lst[0].type() == 'nurbsCurve':
            transform = pm.listRelatives(lst[0], p=True)[0]
            supposed_group = pm.listRelatives(transform, p=True)
            if not supposed_group or supposed_group[0].getShape():
                pm.warning("No group above")
                return
            self.group = supposed_group[0]
            self.group_label.setText(supposed_group[0].name())

        self.blendshape = self.get_existed_blendshape()
        if not self.blendshape:
            self.blendshape = pm.blendShape(self.group)[0]

        # *****************************
        self.get_key_target_dict()

        pm.select(self.blendshape)

    def get_coords_dict(self):
        out_dict = collections.OrderedDict()
        for tr_curve in self.group.getChildren():
            curve_shape = tr_curve.getShape()
            shape_cvs = curve_shape.getCVs()
            out_dict[curve_shape.name()] = collections.OrderedDict()
            for j in range(len(shape_cvs)):
                out_dict[curve_shape.name()]['cv[' + str(j) + ']'] = shape_cvs[j]
        return out_dict

    def get_base_shape(self):
        weights = []
        # flush the weights
        for i in range(self.blendshape.getWeightCount()):
            weights.append(self.blendshape.w[i].get())
            self.blendshape.w[i].set(0.0)
        # get coordinates
        self.base_shape = self.get_coords_dict()
        # restore weight values
        for k, val in enumerate(weights):
            self.blendshape.w[k].set(val)

    def get_key_target_dict(self):
        cur_time = pm.currentTime()
        keys = list(set(pm.keyframe(self.blendshape.w, q=True)))
        for t in keys:
            pm.currentTime(t)
            for i in range(self.blendshape.getWeightCount()):
                if self.blendshape.w[i].get() == 1.0:
                    self.key_target_dict[t] = i
                    break
        pm.currentTime(cur_time)

    def create_target(self):
        idx = mel.eval('string $targetShapes[];doBlendShapeAddTarget("' + self.blendshape.name() + '", 1, 1, "", 1, 0, $targetShapes )')[0]
        return idx

    def rekey(self):
        # keying attributes
        cur_time = pm.currentTime()
        for keyframe, target in self.key_target_dict.items():
            pm.currentTime(keyframe)
            for i in range(self.blendshape.getWeightCount()):
                if i == target:
                    self.blendshape.w[i].set(1.0)
                    self.blendshape.w[i].setKey()
                else:
                    self.blendshape.w[i].set(0.0)
                    self.blendshape.w[i].setKey()
        pm.currentTime(cur_time)

    def store_offsets(self, input_dict, target, store_zero=False):
        # get curves list
        for curve in input_dict:
            curve_index = input_dict.keys().index(curve)
            cv_names = input_dict[curve].keys()
            points = input_dict[curve].values()

            cv_names.insert(0, len(cv_names))
            self.blendshape.it[curve_index].itg[target].iti[6000].ict.set(cv_names, type='componentList')
            if store_zero:
                self.blendshape.it[curve_index].itg[target].iti[6000].ipt.set(0, type='pointArray')
            else:
                self.blendshape.it[curve_index].itg[target].iti[6000].ipt.set(points)

    def edit_clicked(self):
        self.get_base_shape()
        if pm.currentTime() not in self.key_target_dict.keys():
            idx = self.create_target()
            self.key_target_dict[pm.currentTime()] = idx
        else:
            pm.sculptTarget(self.blendshape, e=True, target=self.key_target_dict[pm.currentTime()])

        pm.select(self.group)
        pm.selectType(allObjects=True, allComponents=False, cv=True)
        pm.selectMode(component=True)

    def end_clicked(self):
        pm.sculptTarget(self.blendshape, e=True, target=-1)
        pm.selectType(allObjects=True, allComponents=True)
        pm.selectMode(object=True)
        pm.select(self.blendshape)

        current_dict = self.get_coords_dict()
        difference = collections.OrderedDict()

        for curve in current_dict:
            difference[curve] = collections.OrderedDict()
            for cv_name in current_dict[curve]:
                difference[curve][cv_name] = current_dict[curve][cv_name] - self.base_shape[curve][cv_name]

        self.rekey()
        self.store_offsets(difference, self.key_target_dict[pm.currentTime()])

    def kbs_clicked(self):
        current_dict = self.get_coords_dict()

        if pm.currentTime() not in self.key_target_dict.keys():
            # need to create new target
            idx = self.create_target()
            pm.sculptTarget(self.blendshape, e=True, target=-1)

            # add to key_target_dict
            self.key_target_dict[pm.currentTime()] = idx

            # store 0 offsets
            self.store_offsets(current_dict, idx, store_zero=True)
            self.rekey()

        else:
            # store zeros to offsets
            target = self.key_target_dict[pm.currentTime()]
            self.store_offsets(current_dict, target, store_zero=True)


def create_ui():
    global curve_blendshape_tool_win
    q_maya_window = get_maya_window()
    curve_blendshape_tool_win = MainWidget(parent=q_maya_window)
    curve_blendshape_tool_win.show()
