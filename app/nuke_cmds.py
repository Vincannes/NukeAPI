#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import io_file
from node import Node
from collections import OrderedDict

from pprint import pprint

SCENE_DEFAULT_VALUES = {
    "format": "2048 1556 0 0 2048 1556 1 2K_Super_35(full-ap)",
    "proxy_format": "1024 778 0 0 1024 778 1 1K_Super_35(full-ap)",
    "colorManagement": "Nuke",
    "workingSpaceLUT": "linear",
    "monitorLut": "sRGB",
    "monitorOutLUT": "rec709",
    "int8Lut": "sRGB",
    "int16Lut": "sRGB",
    "logLut": "Cineon",
    "floatLut": "linear",
    "name": ""
}


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

    nuke.scriptSaveAs(test_file_out)
