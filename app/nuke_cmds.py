#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

import io_file
from pprint import pprint
from collections import OrderedDict


class Node(object):
    X_OFFSET = 0
    Y_OFFSET = 50
    DEFAULT_KNOBS = ["name", "inputs", "xpos", "ypos"]

    def __init__(self, class_name, parent):

        self.parent = parent

        self._class_name = class_name
        self._knobs_dict = {}
        for _knob_name in self.DEFAULT_KNOBS:
            if _knob_name == "name":
                value = f"{class_name}1"
            elif _knob_name in ["xpos", "ypos"]:
                values = self._get_positions()
                value = values[0] if _knob_name == "xpos" else values[1]
            else:
                value = 0
            self._knobs_dict[_knob_name] = value

    def Class(self):
        return self._class_name

    def setXYPos(self, x, y):
        self._knobs_dict["xpos"] = x
        self._knobs_dict["ypos"] = y
        self.parent.scene[self._class_name] = self._knobs_dict

    def setInput(self, index=0, node=None):
        if "inputs" in self._knobs_dict.keys():
            self._knobs_dict.pop("inputs")

        if self._class_name in self.parent.scene.keys():
            self.parent.scene[self._class_name] = dict(self._knobs_dict)
            key_order = list(self.parent.scene.keys())
            key_order.remove(node.Class())
            key_order.insert(key_order.index(self._class_name), node.Class())
            self.parent.scene = OrderedDict((key, self.parent.scene[key]) for key in key_order)

    def get_node_dict(self):
        return self._knobs_dict

    def xpos(self):
        return self._knobs_dict.get("xpos")

    def ypos(self):
        return self._knobs_dict.get("ypos")

    def _get_positions(self):
        xpos = 0
        ypos = 0
        for node, data in self.parent.scene.items():
            _xpos = data.get("xpos", 0)
            _ypos = data.get("ypos", 0)
            xpos += _xpos + self.X_OFFSET
            ypos += _ypos + self.Y_OFFSET
        return xpos, ypos


class NukeCmds(object):

    def __init__(self, scene=None):
        self.scene = scene
        if scene is None:
            self.scene = OrderedDict()

    def createNode(self, name):
        _node = Node(name, self)
        self.scene[name] = _node.get_node_dict()
        return _node


if __name__ == '__main__':
    # TODO if multiple same Class node (check with name)
    test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final_2.nk"

    nuke = NukeCmds()
    check = nuke.createNode("CheckerBoard")
    grade = nuke.createNode("Grade")
    noop = nuke.createNode("NoOp")
    pprint(nuke.scene)
    grade.setInput(0, noop)
    grade.setXYPos(noop.xpos(), noop.ypos() + 50)
    pprint(nuke.scene)

    io_file.dict_to_nk_scene(nuke.scene, test_file_out)
