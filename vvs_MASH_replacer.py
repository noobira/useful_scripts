from maya import cmds
from collections import OrderedDict
import MASH.api as mapi


# this module replaces repeating mesh geometry to mash instances
# select list of (several types) geo and then add to selection the mesh of each type at last for making instances of (they will be hidden after)
# and run go_process()

class MyObj(object):
    def __init__(self, name_val, tran_val, rot_val, scl_val):
        self.name = name_val
        self.tran = tran_val
        self.rot = rot_val
        self.scl = scl_val

    def my_print(self):
        print("[" + self.name + ']:')
        print("   .tran=" + str(self.tran))
        print("   .rot=" + str(self.rot))
        print("   .scl=" + str(self.scl))


# func that generating code to put into mash script node
def generate_code(some_dict):
    code = 'import openMASH\nmd = openMASH.MASHData(thisNode)\n'
    mash_position = 0
    for i, key in enumerate(some_dict):
        row_length = len(some_dict[key]) - 1
        for j in range(row_length):
            code += 'md.outPosition[' + str(mash_position) + '] = ' + str(some_dict[key][j].tran) + '\n'
            code += 'md.outRotation[' + str(mash_position) + '] = ' + str(some_dict[key][j].rot) + '\n'
            code += 'md.outScale[' + str(mash_position) + '] = ' + str(some_dict[key][j].scl) + '\n'
            code += 'md.id[' + str(mash_position) + '] = ' + str(i) + '\n'
            mash_position += 1
    code += 'md.setData()'
    return code


def get_mesh_element_count(some_dict):
    length = 0
    for key in some_dict.keys():
        length += len(some_dict[key]) - 1

    return length


# main function to execute
def go_process():
    list_obj = cmds.ls(sl=True)
    if len(list_obj) < 2:
        cmds.warning('Select 2 or more objects')
        return

    if not cmds.pluginInfo('MASH.mll', q=True, l=True):
        cmds.loadPlugin('MASH.mll')

    my_dict = OrderedDict()
    for obj in list_obj:
        if (not cmds.listRelatives(obj, s=True)) and cmds.nodeType(obj) == 'transform':
            for x in cmds.listRelatives(obj, c=True, type='transform'):
                poligons = cmds.polyEvaluate(x, f=True)
                my_obj = MyObj(x, cmds.xform(x, q=True, t=True, ws=True), cmds.xform(x, q=True, ro=True, ws=True), cmds.xform(x, q=True, s=True, ws=True))
                if not my_dict.get(poligons):
                    my_dict[poligons] = [my_obj]
                else:
                    my_dict[poligons].append(my_obj)
        else:
            poligons = cmds.polyEvaluate(obj, f=True)
            my_obj = MyObj(obj, cmds.xform(obj, q=True, t=True, ws=True), cmds.xform(obj, q=True, ro=True, ws=True), cmds.xform(obj, q=True, s=True, ws=True))
            if not my_dict.get(poligons):
                my_dict[poligons] = [my_obj]
            else:
                my_dict[poligons].append(my_obj)

    last_nodes = []
    for key in my_dict.keys():
        last_nodes.append(my_dict[key][-1])

    cmds.select(cl=True)
    cmds.optionVar(iv=('mOGTN', 2))

    mash_network = mapi.Network()
    mash_network.createNetwork('MYMASH')

    mash_node = mash_network.waiter
    distr_node = mash_network.distribute
    instancer_node = mash_network.instancer
    python_node = mash_network.addNode('MASH_Python').name

    for i, ln in enumerate(last_nodes):
        cmds.connectAttr(ln.name + '.matrix', instancer_node + '.inputHierarchy[' + str(i) + ']')

    length = get_mesh_element_count(my_dict)

    cmds.setAttr(distr_node + '.pointCount', length)

    s = generate_code(my_dict)
    cmds.setAttr(python_node + '.pyScript', s, type="string")

    for x in list_obj:
        cmds.setAttr(x + '.visibility', 0)
