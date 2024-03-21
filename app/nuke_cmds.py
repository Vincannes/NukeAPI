#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from node import Node
from io_file import SceneDict
from collections import OrderedDict

from pprint import pprint


class NukeCmds(object):
    SKIP_NODES_TYPE = ["version", "Root", "define_window_layout_xml", "add_layer", "clone"]

    def __init__(self, scene=None):
        if scene is None:
            self._scene = None
            self._dict_scene = OrderedDict()
            self._all_nodes = []
        else:
            self._scene = self.scriptOpen(scene)
            self._dict_scene = self._scene.get_dict()
            self._all_nodes = self._get_all_nodes()

    @property
    def scene(self):
        return self._dict_scene

    def allNodes(self, filter=None, recursiveGroups=False):
        if filter and not recursiveGroups: # si filtre et pas groups
            _nodes = [n for n in self._all_nodes if n.Class() == filter and not n.parent_node]
        elif recursiveGroups: # si groups et pas filtre
            _nodes = self._all_nodes
        elif filter and recursiveGroups: # si filtre et groups
            _nodes = [n for n in self._all_nodes if n.Class() == filter]
        else: # tous les nodes hors groups
            _nodes = [n for n in self._all_nodes if not n.parent_node]
        return _nodes

    def createNode(self, name):
        _node = Node(name, self)
        self._dict_scene[_node.subClass()] = _node.get_node_dict()
        return _node

    def root(self):
        knobs = self._dict_scene.get("Root")
        _node = Node("Root", self)
        _node.build_node_from_data(knobs)
        return _node

    def selectedNode(self):
        """
        Returns the ‘node the user is thinking about’.
        If several nodes are selected, this returns one of them.
        The one returned will be an ‘output’ node in that no other
        selected nodes use that node as an input.
        :return:
        """
        return self.selectedNodes()[-1]

    def selectedNodes(self):
        return [i for i in self.allNodes() if i.isSelected()]

    def scriptSaveAs(self, path):
        self._set_root(path)
        io_file.dict_to_nk_scene(self._dict_scene, path)

    def scriptOpen(self, path):
        return SceneDict(path)

    def toNode(self, node_name):
        return next((node for node in self.allNodes() if node_name == node.name()), None)

    # PRIVATES

    def _get_connected_nodes(self):
        _input_nodes = {}
        pprint(self._scene.get_inputs())
        for node_name, datas in self._scene.get_inputs().items():
            object_node = datas.get("object")
            node = next((node for node in self._all_nodes if node_name == node.name()), None)
            if object_node:
                node.object = object_node
            if not node_name in _input_nodes.keys():
                _input_nodes[node_name] = []
            for dependent_name in datas.get("dependents"):
                dependent_node = self.toNode(dependent_name)
                _input_nodes[node_name].append(dependent_node)
        return _input_nodes

    def _set_root(self, path):
        _root_node = Node("Root", self)
        _root_node.knob("name").setValue(path)
        self._dict_scene[_root_node.subClass()] = _root_node.get_node_dict()
        self._dict_scene.move_to_end(_root_node.subClass(), last=False)

    def _get_all_nodes(self):
        all_nodes = []
        _grp_nodes = []
        for node_class, reads in self._dict_scene.items():
            if node_class in self.SKIP_NODES_TYPE:
                continue
            for node_name, knobs in reads.items():
                _node = Node(node_class, self)
                _node.build_node_from_data(knobs)
                all_nodes.append(_node)
                if node_class == "Group":
                    _grp_nodes.append(_node)
                    _node.set_group_nodes(knobs.get("nodes"))

        for grp_node in _grp_nodes:
            _nodes = []
            for _node_name in grp_node.group_nodes:
                _node = next(
                    (node for node in all_nodes if _node_name == node.name()), None
                )
                _node.set_parent_node(grp_node)
                _nodes.append(_node)
            grp_node.set_group_nodes(_nodes)

        return all_nodes


nuke = NukeCmds()

if __name__ == '__main__':
    test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final_2.nk"
    path_test_file = "D:\\Desk\\python\\NukeAPI\\tests\\083_060-cmp-base-v016.nk"
    # path_test_file = "D:\\Desk\\python\\NukeAPI\\tests\\083_060-cmp-base-v017.nk"

    # nuke = NukeCmds()
    # read = nuke.createNode("Read")
    # check = nuke.createNode("CheckerBoard")
    # grade = nuke.createNode("Grade")
    # noop = nuke.createNode("NoOp")
    # noop2 = nuke.createNode("NoOp")
    #
    # read.knob("file").setValue("kdkdkdkdkdkd")
    # grade.setInput(0, noop)
    # grade.setXYPos(noop.xpos(), noop.ypos() + 50)
    # noop2.setXYPos(250, 53)
    #
    # grade.setSelected(True)
    # noop2.setSelected(True)
    #
    # print("")
    # print([i.name() for i in nuke.allNodes()])
    # print([i.name() for i in nuke.selectedNodes()])
    #
    # nuke.scriptSaveAs(test_file_out)

    nuke = NukeCmds(path_test_file)
    print("")
    pprint(nuke._get_connected_nodes())
    print("")
    # pprint(nuke.allNodes())
    # print(nuke.root().name())
    # print(nuke.allNodes())
    node = nuke.toNode("Link_cam_3D1")
    print(node)
    print(node.dependent())
    # print(node.knob("xpos").value())
    # for i in node.group_nodes:
    #     print(i.name(), i.parent_node.name())