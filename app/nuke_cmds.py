#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import io_file
from node import Node
from collections import OrderedDict

from pprint import pprint


class NukeCmds(object):

    def __init__(self, scene=None):
        self.scene = scene
        if scene is None:
            self.scene = OrderedDict()

    def createNode(self, name):
        _node = Node(name, self)
        self.scene[_node.subClass()] = _node.get_node_dict()
        return _node

    def allNodes(self):
        all_nodes = []
        for node, datas in self.scene.items():
            _node = Node(node, self)
            _node.build_node_from_data(datas)
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
        io_file.dict_to_nk_scene(self.scene, path)

    # PRIVATES

    def _set_root(self, path):
        _root_node = Node("Root", self)
        _root_node.knob("name").setValue(path)
        self.scene[_root_node.subClass()] = _root_node.get_node_dict()
        self.scene.move_to_end(_root_node.subClass(), last=False)


if __name__ == '__main__':
    test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final_2.nk"

    nuke = NukeCmds()
    read = nuke.createNode("Read")
    check = nuke.createNode("CheckerBoard")
    grade = nuke.createNode("Grade")
    noop = nuke.createNode("NoOp")
    noop2 = nuke.createNode("NoOp")

    read.knob("file").setValue("kdkdkdkdkdkd")
    grade.setInput(0, noop)
    grade.setXYPos(noop.xpos(), noop.ypos() + 50)
    noop2.setXYPos(250, 53)

    grade.setSelected(True)
    noop2.setSelected(True)

    print("")
    print([i.name() for i in nuke.allNodes()])
    print([i.name() for i in nuke.selectedNodes()])

    nuke.scriptSaveAs(test_file_out)
