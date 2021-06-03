import pymel.core as pm

# some ik spine installation on rig with only fk spine (names are hardcoded, so should be replaced)


def replace_hierarchy(from_obj, to_obj, exceptions=None):
    children = pm.listRelatives(from_obj, c=True)
    for j in children:
        if len(j.type(i=True)) > 1 and j.type(i=True)[-2] == "constraint":
            continue
        if len(j.type(i=True)) > 3 and j.type(i=True)[3] == "shape":
            continue
        if exceptions and (j in exceptions):
            continue
        j.setParent(to_obj)


def swap_out_connections(from_obj, to_obj, exceptions=None):
    conns = list(set(from_obj.connections(c=True, p=True, s=False, d=True)) - set(from_obj.connections(c=True, p=True, s=False, d=True, t=["objectSet"])))
    # reconnect not constraint attrs
    for out_plug, in_plug in conns:
        if exceptions and (in_plug.node() in exceptions):
            continue
        if in_plug.attrName(longName=True) in ["constraintParentInverseMatrix", "constraintRotateOrder", "constraintRotatePivot", "constraintRotateTranslate", "constraintScaleCompensate", "constraintJointOrient"]:
            continue
        to_obj.attr(out_plug.attrName()).connect(in_plug, f=True)


def process():
    # 1
    spine_ik_00_jnt = pm.duplicate("Md_Spine_00_JNT", po=True, n="Md_SpineIK_00_JNT")[0]
    spine_ik_00_jnt.setParent(None)
    spine_ik_00_jnt.segmentScaleCompensate.set(1)
    spine_ik_01_jnt = pm.duplicate("Md_Spine_01_JNT", po=True, n="Md_SpineIK_01_JNT")[0]
    spine_ik_01_jnt.setParent(None)
    spine_ik_01_jnt.segmentScaleCompensate.set(1)
    spine_ik_02_jnt = pm.duplicate("Md_Spine_02_JNT", po=True, n="Md_SpineIK_02_JNT")[0]
    spine_ik_02_jnt.setParent(None)
    spine_ik_02_jnt.segmentScaleCompensate.set(1)
    chest_ik_hlp = pm.duplicate("Md_Chest_JNT", po=True, n="Md_ChestIK_JNTHlp")[0]
    chest_ik_hlp.setParent(None)
    chest_ik_hlp.segmentScaleCompensate.set(1)
    chest_ik_end = pm.duplicate(chest_ik_hlp, n="Md_ChestIK_JNTEnd")[0]
    chest_ik_end.setParent(None)
    chest_ik_end.segmentScaleCompensate.set(1)

    # 2
    aim0 = pm.aimConstraint(spine_ik_01_jnt, spine_ik_00_jnt, aim=[0, 1, 0], u=[0, 0, 1], wuo=spine_ik_01_jnt)
    aim1 = pm.aimConstraint(spine_ik_02_jnt, spine_ik_01_jnt, aim=[0, 1, 0], u=[0, 0, 1], wuo=spine_ik_02_jnt)
    aim2 = pm.aimConstraint(chest_ik_hlp, spine_ik_02_jnt, aim=[0, 1, 0], u=[0, 0, 1], wuo=chest_ik_hlp)
    pm.delete([aim0, aim1, aim2])
    spine_ik_01_jnt.setParent(spine_ik_00_jnt)
    spine_ik_02_jnt.setParent(spine_ik_01_jnt)
    chest_ik_hlp.setParent(spine_ik_02_jnt)
    chest_ik_end.setParent(chest_ik_hlp)

    # 3
    crv = pm.curve(p=[spine_ik_00_jnt.getTranslation(space="world"), spine_ik_01_jnt.getTranslation(space="world"), spine_ik_02_jnt.getTranslation(space="world"), chest_ik_end.getTranslation(space="world")], n="IKSpline_crv")
    ik_handle = pm.ikHandle(sj=spine_ik_00_jnt, ee=chest_ik_end, roc=True, n="spline_ikHandle", c=crv, ccv=False, pcv=False, sol='ikSplineSolver')[0]
    crv.inheritsTransform.set(0)

    # 4
    up_con = pm.curve(d=1, n="Md_IKSpine_Up_CON", p=[(-1, 2, 1), (1, 2, 1), (1, 2, -1), (-1, 2, -1), (-1, 2, 1), (-1, 0, 1), (-1, 0, -1), (-1, 2, -1), (-1, 2, 1), (-1, 0, 1), (1, 0, 1), (1, 2, 1), (1, 2, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1), (-1, 0, -1), (1, 0, -1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    down_con = pm.curve(d=1, n="Md_IKSpine_Down_CON", p=[(-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    up_con.getShape().overrideEnabled.set(1)
    up_con.getShape().overrideColor.set(13)
    down_con.getShape().overrideEnabled.set(1)
    down_con.getShape().overrideColor.set(13)

    chest_con = pm.PyNode("Md_Chest_CON")
    up_grp = pm.group(em=True, n="Md_IKSpine_Up_GRP")
    down_grp = pm.group(em=True, n="Md_IKSpine_Down_GRP")
    up_grp.setTranslation(chest_con.getTranslation(space="world"))
    down_grp.setTranslation(spine_ik_00_jnt.getTranslation(space="world"))
    up_con.setParent(up_grp)
    down_con.setParent(down_grp)
    up_con.setTranslation([0, 0, 0])
    down_con.setTranslation([0, 0, 0])

    # 5
    loc0 = pm.spaceLocator(n="IKSpline_cv0")
    loc1 = pm.spaceLocator(n="IKSpline_cv1")
    loc2 = pm.spaceLocator(n="IKSpline_cv2")
    loc3 = pm.spaceLocator(n="IKSpline_cv3")
    loc0.setTranslation(crv.cv[0].getPosition(space="world"))
    loc1.setTranslation(crv.cv[1].getPosition(space="world"))
    loc2.setTranslation(crv.cv[2].getPosition(space="world"))
    loc3.setTranslation(crv.cv[3].getPosition(space="world"))
    loc0.setParent(down_con)
    loc1.setParent(down_con)
    loc2.setParent(up_con)
    loc3.setParent(up_con)
    loc0.worldPosition[0].connect(crv.controlPoints[0])
    loc1.worldPosition[0].connect(crv.controlPoints[1])
    loc2.worldPosition[0].connect(crv.controlPoints[2])
    loc3.worldPosition[0].connect(crv.controlPoints[3])

    # 6
    ik_handle.dTwistControlEnable.set(1)
    ik_handle.dWorldUpType.set(4)
    ik_handle.dForwardAxis.set(2)
    ik_handle.dWorldUpAxis.set(3)
    ik_handle.dWorldUpVector.set([0, 0, 1])
    ik_handle.dWorldUpVectorEnd.set([0, 0, 1])
    loc0.wm.connect(ik_handle.dwum)
    loc3.wm.connect(ik_handle.dwue)

    # 7
    chest_ik_jnt = pm.duplicate(chest_ik_end, n="Md_ChestIK_JNT")[0]
    chest_ik_jnt.setParent(chest_ik_hlp)
    pm.orientConstraint(up_con, chest_ik_jnt, mo=True)

    # 8
    skeleton_grp = pm.group(em=True, n="IKSpline_skeleton")
    crv.setParent(skeleton_grp)
    ik_handle.setParent(skeleton_grp)
    spine_ik_00_jnt.setParent(skeleton_grp)
    pm.parentConstraint(down_con, skeleton_grp, mo=True)

    # 9
    spine_con = pm.curve(d=1, n="Md_Spine_CON",
                                p=[(-0.51105675673734918, 0.073002262339498566, 0),
                                    (-0.073002262339498566, 0.073002262339498566, 0),
                                    (-0.073002262339498566, 0.51105675673734918, 0),
                                    (0.073002262339498566, 0.51105675673734918, 0),
                                    (0.073002262339498566, 0.073002262339498566, 0),
                                    (0.51105675673734918, 0.073002262339498566, 0),
                                    (0.51105675673734918, -0.073002262339498566, 0),
                                    (0.073002262339498566, -0.073002262339498566, 0),
                                    (0.073002262339498566, -0.51105675673734918, 0),
                                    (-0.073002262339498566, -0.51105675673734918, 0),
                                    (-0.073002262339498566, -0.073002262339498566, 0),
                                    (-0.51105675673734918, -0.073002262339498566, 0),
                                    (-0.51105675673734918, 0.073002262339498566, 0)],
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    spine_con.getShape().overrideEnabled.set(1)
    spine_con.getShape().overrideColor.set(6)

    for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]:
        spine_con.attr(a).setKeyable(False)
        spine_con.attr(a).showInChannelBox(False)
    spine_con.addAttr("FK_IK_blend", at="float", k=True, minValue=0.0, maxValue=1.0)
    spine_con.addAttr("FK_IK_Visible", at="float", minValue=0.0, maxValue=1.0)
    spine_con.FK_IK_Visible.showInChannelBox(True)
    spine_con.addAttr("IKStretch", at="float", k=True, minValue=0.0, maxValue=1.0)

    spine_grp = pm.group(em=True, n="Md_Spine_GRP")
    spine_con.setParent(spine_grp)

    middle_point = (up_con.getTranslation(space="world") + down_con.getTranslation(space="world")) / 2

    spine_grp.setTranslation([middle_point.x + 2, middle_point.y, middle_point.z], space="world")

    spine_con.FK_IK_blend.set(1)
    spine_con.FK_IK_Visible.set(1)
    spine_con.IKStretch.set(1)

    # 10
    if not pm.pluginInfo("lookdevKit", q=True, loaded=True):
        pm.loadPlugin("lookdevKit")
    crv_shape = crv.getShape()
    curve_info = pm.createNode("curveInfo", n="curveInfo_IKSpline")
    crv_shape.ws[0].connect(curve_info.inputCurve)
    percent_length_math = pm.createNode("floatMath", n="percentLength_IKSpline")
    percent_length_math.operation.set(3)
    curve_info.arcLength.connect(percent_length_math.floatA)
    percent_length_math.floatB.set(percent_length_math.floatA.get())
    substract_math = pm.createNode("floatMath", n="substract_IKSpline")
    substract_math.operation.set(1)
    percent_length_math.outFloat.connect(substract_math.floatA)
    mult_math = pm.createNode("floatMath", n="mult_IKSpline")
    mult_math.operation.set(2)
    substract_math.outFloat.connect(mult_math.floatB)
    spine_con.IKStretch.connect(mult_math.floatA)
    add_math = pm.createNode("floatMath", n="add_IKSpline")
    add_math.operation.set(0)
    mult_math.outFloat.connect(add_math.floatA)
    add_math.outFloat.connect(spine_ik_00_jnt.sy)
    add_math.outFloat.connect(spine_ik_01_jnt.sy)
    add_math.outFloat.connect(spine_ik_02_jnt.sy)

    # 11
    pm.parentConstraint("Md_HipGimbal_01_CON", loc0, mo=True)
    # pm.parentConstraint("Md_HipGimbal_01_CON", loc0)

    # 12
    up_grp.setParent("Md_RootX_CON")
    down_grp.setParent("Md_RootX_CON")
    spine_grp.setParent("Md_RootX_CON")
    skeleton_grp.setParent("Md_Hip_00_JNT")

    # 13
    fk_jnt0 = pm.rename("Md_Spine_00_JNT", "Md_FKSpine_00_JNT")
    fk_jnt1 = pm.rename("Md_Spine_01_JNT", "Md_FKSpine_01_JNT")
    fk_jnt2 = pm.rename("Md_Spine_02_JNT", "Md_FKSpine_02_JNT")
    fk_chest = pm.rename("Md_Chest_JNT", "Md_FKChest_JNT")

    # 14
    new_jnt0 = pm.duplicate("Md_FKSpine_00_JNT", n="Md_Spine_00_JNT", po=True, ic=False)[0]
    new_jnt0.setParent("Md_Hip_00_JNT")
    new_jnt1 = pm.duplicate("Md_FKSpine_01_JNT", n="Md_Spine_01_JNT", po=True, ic=False)[0]
    new_jnt1.setParent(new_jnt0)
    new_jnt2 = pm.duplicate("Md_FKSpine_02_JNT", n="Md_Spine_02_JNT", po=True, ic=False)[0]
    new_jnt2.setParent(new_jnt1)
    new_chest_jnt = pm.duplicate("Md_FKChest_JNT", n="Md_Chest_JNT", po=True, ic=False)[0]
    new_chest_jnt.setParent(new_jnt2)

    # 15
    replace_hierarchy(fk_jnt0, new_jnt0, [fk_jnt1])
    replace_hierarchy(fk_jnt1, new_jnt1, [fk_jnt2])
    replace_hierarchy(fk_jnt2, new_jnt2, [fk_chest])
    replace_hierarchy(fk_chest, new_chest_jnt)
    replace_hierarchy(chest_con, new_chest_jnt, [pm.PyNode("Md_ChestOffset_CON")])

    swap_out_connections(fk_jnt0, new_jnt0, [fk_jnt1])
    swap_out_connections(fk_jnt1, new_jnt1, [fk_jnt2])
    swap_out_connections(fk_jnt2, new_jnt2, [fk_chest])
    swap_out_connections(fk_chest, new_chest_jnt)
    # swap_out_connections(chest_con, new_chest_jnt)

    # 16
    pc0 = pm.parentConstraint(fk_jnt0, spine_ik_00_jnt, new_jnt0, mo=True)
    pc0.interpType.set(2)
    rev0 = pm.createNode('reverse')
    spine_con.FK_IK_blend.connect(pc0.Md_SpineIK_00_JNTW1, f=True)
    spine_con.FK_IK_blend.connect(rev0.inputX)
    rev0.outputX.connect(pc0.Md_FKSpine_00_JNTW0, f=True)

    pc1 = pm.parentConstraint(fk_jnt1, spine_ik_01_jnt, new_jnt1, mo=True)
    pc1.interpType.set(2)
    spine_con.FK_IK_blend.connect(pc1.Md_SpineIK_01_JNTW1, f=True)
    rev0.outputX.connect(pc1.Md_FKSpine_01_JNTW0, f=True)

    pc2 = pm.parentConstraint(fk_jnt2, spine_ik_02_jnt, new_jnt2, mo=True)
    pc2.interpType.set(2)
    spine_con.FK_IK_blend.connect(pc2.Md_SpineIK_02_JNTW1, f=True)
    rev0.outputX.connect(pc2.Md_FKSpine_02_JNTW0, f=True)

    pc3 = pm.parentConstraint(fk_chest, chest_ik_jnt, new_chest_jnt, mo=True)
    pc3.interpType.set(2)
    spine_con.FK_IK_blend.connect(pc3.Md_ChestIK_JNTW1, f=True)
    rev0.outputX.connect(pc3.Md_FKChest_JNTW0, f=True)

    # 17
    hip_pivot_grp = pm.group(em=True, n="Md_Hip_FK_PivotGRP")
    root = pm.PyNode("Md_RootX_CON")
    hip_pivot_grp.setTranslation(root.getTranslation(space="world"), space="world")
    hip_pivot_grp.setParent(root)

    pc4 = pm.parentConstraint(down_con, hip_pivot_grp, "Md_Hip_00_GRP", mo=True)
    pc4.interpType.set(2)
    spine_con.FK_IK_blend.connect(pc4.Md_IKSpine_Down_CONW0, f=True)
    rev0.outputX.connect(pc4.Md_Hip_FK_PivotGRPW1, f=True)

    # 18
    blend2 = pm.createNode("blendTwoAttr")
    blend3 = pm.createNode("blendTwoAttr")
    rev2 = pm.createNode("reverse")
    spine_con.FK_IK_Visible.connect(rev2.inputX)
    spine_con.FK_IK_blend.connect(rev2.inputY)
    rev2.outputX.connect(blend2.input[0])
    rev2.outputY.connect(blend3.input[1])
    spine_con.FK_IK_Visible.connect(blend2.attributesBlender)
    spine_con.FK_IK_Visible.connect(blend3.attributesBlender)
    spine_con.FK_IK_blend.connect(blend2.input[1])
    blend3.input[0].set(1)
    blend2.output.connect(up_grp.visibility)
    blend2.output.connect(down_grp.visibility)
    grp_temp = pm.PyNode("Md_Spine_00_GRP")
    blend3.output.connect(grp_temp.visibility)
