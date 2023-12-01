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

    def scriptSaveAs(self, path):
        io_file.dict_to_nk_scene(self.scene, path)


if __name__ == '__main__':
    test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final_2.nk"

    nuke = NukeCmds()
    read = nuke.createNode("Read")
    check = nuke.createNode("CheckerBoard")
    grade = nuke.createNode("Grade")
    noop = nuke.createNode("NoOp")
    noop2 = nuke.createNode("NoOp")

    pprint(nuke.scene)
    print("")

    read.knob("file").setValue("kdkdkdkdkdkd")
    grade.setInput(0, noop)
    grade.setXYPos(noop.xpos(), noop.ypos() + 50)
    noop2.setXYPos(250, 53)
    # noop2.setInput(0, check)
    print(read.knob("file").value())
    pprint(nuke.scene)
    nuke.scriptSaveAs(test_file_out)
