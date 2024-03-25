#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from node import Node
from io_file import SceneDict
from collections import OrderedDict

from pprint import pprint


class NukeCmds(object):
    SKIP_NODES_TYPE = ["version", "define_window_layout_xml", "add_layer", "clone"]

    def __init__(self, scene=None):
        if scene is None:
            self._scene = None
            self._nodes_scene = OrderedDict()
            self._all_nodes = []
        else:
            self._scene = self.scriptOpen(scene)
            self._nodes_scene = self._scene.get_nodes()
            self._all_nodes = self._get_all_nodes()

    @property
    def scene(self):
        return self._nodes_scene

    def allNodes(self, filter=None, recursiveGroups=False):
        if filter and not recursiveGroups:# si filtre et pas groups
            _nodes = [n for n in self._all_nodes if n.Class() == filter and not n.parent_node]
        elif recursiveGroups: # si groups et pas filtre
            _nodes = self._all_nodes
        elif filter and recursiveGroups:# si filtre et groups
            _nodes = [n for n in self._all_nodes if n.Class() == filter]
        else:# tous les nodes hors groups
            _nodes = [n for n in self._all_nodes if not n.parent_node]
        return _nodes

    # def createNode(self, name):
    #     _node = Node(name, self)
    #     self._dict_scene[_node.subClass()] = _node.get_node_dict()
    #     return _node

    def root(self):
        _node = next(
            (node for node in self._all_nodes if node.Class() == "Root")
        )
        return _node

    def selectedNode(self):
        """
        Returns the node the user is thinking about.
        If several nodes are selected, this returns one of them.
        The one returned will be an output node in that no other
        selected nodes use that node as an input.
        :return:
        """
        return self.selectedNodes()[-1]

    def selectedNodes(self):
        return [i for i in self.allNodes() if i.isSelected()]

    # def scriptSaveAs(self, path):
    #     self._set_root(path)
    #     io_file.dict_to_nk_scene(self._dict_scene, path)

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
            print(node_name, node)
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
        self._all_nodes.append(_root_node)

    def _get_all_nodes(self):
        all_nodes = []
        for node_dict in self._nodes_scene:
            for node_name, knobs in node_dict.items():
                if node_name in self.SKIP_NODES_TYPE or knobs.get("Class", node_name) in self.SKIP_NODES_TYPE:
                    continue
                node_class = knobs.get("Class", node_name)
                _node = Node(node_class, self)
                _node.build_node_from_data(knobs)
                all_nodes.append(_node)
                if node_class in ["Group", "Gizmo"]:
                    _grp_nodes = []
                    for _sub_grp in knobs.get("nodes"):
                        for _sub_node_name, _sub_data in _sub_grp.items():
                            _sub_grp_node = Node(_sub_data.get("Class"), self)
                            _sub_grp_node.build_node_from_data(_sub_data)
                            _sub_grp_node.set_parent_node(_node)
                            _grp_nodes.append(_sub_grp_node)
                    _node.set_group_nodes(_grp_nodes)

        return all_nodes


nuke = NukeCmds()

if __name__ == '__main__':
    import os
    this_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_out = os.path.join(os.path.dirname(this_dir), "tests", "test_final_2.nk")
    path_test_file = os.path.join(os.path.dirname(this_dir), "tests", "083_060-cmp-base-v016.nk")
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
    nuke = NukeCmds("/homes/trolardv/Documents/doc_delivery/0089_mou_0010-vzero-base-v003.nk")
    # nuke.scriptSaveAs(test_file_out)
    # node = nuke.toNode("Switch2")
    # pprint(nuke.scene.get("Switch"))
    # pprint(nuke.scene.get("Group"))
    # print(node)
    print("")
    # pprint(nuke._get_connected_nodes())
    # print("")
    # pprint(nuke.allNodes())
    print(len(nuke.allNodes()))
    print(nuke.root())
    print(nuke.root().name())
    # print(nuke.allNodes())
    node = nuke.toNode("Link_cam_3D1")
    print(node)
    # print(node.dependent())
    # print(node.knob("xpos").value())
    # for i in node.group_nodes:
    #     print(i.name(), i.parent_node.name())