#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from node import Node
from io_file import SceneDict
from collections import OrderedDict

from pprint import pprint


class NukeCmds(object):
    SKIP_NODES_TYPE = ["version", "Root", "define_window_layout_xml", "add_layer"]

    def __init__(self, scene=None):
        if scene is None:
            self._scene = None
            self._dict_scene = OrderedDict()
            self._all_nodes = []
        else:
            self._scene = self.scriptOpen(scene)
            self._dict_scene = self._scene.get_dict()
            self._all_nodes = self.allNodes()

    @property
    def scene(self):
        return self._dict_scene

    def createNode(self, name):
        _node = Node(name, self)
        self._dict_scene[_node.subClass()] = _node.get_node_dict()
        return _node

    def toNode(self, node_name):
        return next((node for node in self._all_nodes if node_name == node.name()), None)

    def allNodes(self):
        all_nodes = []
        for node_class, reads in self._dict_scene.items():
            if node_class in self.SKIP_NODES_TYPE:
                continue
            for node_name, knobs in reads.items():
                _node = Node(node_class, self)
                _node.build_node_from_data(knobs)
                all_nodes.append(_node)
        return all_nodes

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

    # PRIVATES

    def _set_root(self, path):
        _root_node = Node("Root", self)
        _root_node.knob("name").setValue(path)
        self._dict_scene[_root_node.subClass()] = _root_node.get_node_dict()
        self._dict_scene.move_to_end(_root_node.subClass(), last=False)


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
    # pprint(nuke.allNodes())
    print(nuke.allNodes())
    node = nuke.toNode("Link_leaves_proj2")
    print(node.knob("label").value())
    print(node.knob("hide_input").value())
    print(node.knob("Tlink").value())