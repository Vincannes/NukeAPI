#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re
import io_file
import regex_wrapper as regw
from pprint import pprint
from collections import OrderedDict


class Knob(object):

    def __init__(self, name, defaut_val="", parent=None):
        self.name = name
        self._value = defaut_val
        self._parent = parent

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value
        self._parent._knobs_dict[self.name] = value


class Node(object):
    X_OFFSET = 0
    Y_OFFSET = 50
    DEFAULT_KNOBS = ["name", "inputs", "xpos", "ypos"]

    def __init__(self, class_name, parent):

        self.parent = parent

        self._class_name = class_name
        self._knobs_dict = {}
        self._knobs_object = {}

        self._get_node_from_dict()

        for _knob_name in self.DEFAULT_KNOBS:
            if _knob_name == "name":
                value = self._generate_name()
            elif _knob_name in ["xpos", "ypos"]:
                values = self._get_positions()
                value = values[0] if _knob_name == "xpos" else values[1]
            else:
                value = 0
            _knob = Knob(_knob_name, parent=self)
            _knob.setValue(value)
            self._knobs_dict[_knob_name] = value
            self._knobs_object[_knob_name] = _knob

        self._sub_class_name = f"[{self._get_index()}]{class_name}"

    def knob(self, knob_name):
        if knob_name not in self._knobs_object:
            self._knobs_dict[knob_name] = 0
            self._knobs_object[knob_name] = Knob(knob_name, parent=self)
        return self._knobs_object.get(knob_name)

    def Class(self):
        return self._class_name

    def subClass(self):
        return self._sub_class_name

    def setXYPos(self, x, y):
        self._knobs_dict["xpos"] = x
        self._knobs_dict["ypos"] = y
        self.parent.scene[self._sub_class_name] = self._knobs_dict

    def setInput(self, index=0, node=None):
        if "inputs" in self._knobs_dict.keys():
            self._knobs_dict.pop("inputs")

        if self._sub_class_name in self.parent.scene.keys():
            node_to_place_before = node.subClass()
            self.parent.scene[self._sub_class_name] = dict(self._knobs_dict)
            key_order = list(self.parent.scene.keys())
            key_order.remove(node_to_place_before)
            key_order.insert(key_order.index(self._sub_class_name), node_to_place_before)
            self.parent.scene = OrderedDict((key, self.parent.scene[key]) for key in key_order)

    def get_node_dict(self):
        return self._knobs_dict

    def xpos(self):
        return self._knobs_dict.get("xpos")

    def ypos(self):
        return self._knobs_dict.get("ypos")

    # PRIVATES

    def _get_positions(self):
        xpos = 0
        ypos = 0
        for node, data in self.parent.scene.items():
            _xpos = data.get("xpos", 0)
            _ypos = data.get("ypos", 0)
            xpos += _xpos + self.X_OFFSET
            ypos += _ypos + self.Y_OFFSET
        return xpos, ypos

    def _get_index(self):
        return len(self._get_node_from_dict())

    def _generate_name(self):
        names_iter = [0]
        for n in self._get_node_from_dict():
            _name = n.get("name")
            _int = int(re.search(r'(\d+)', _name).group(1))
            names_iter.append(_int)
        index_name = max(names_iter) + 1
        return self._class_name + str(index_name)

    def _get_node_from_dict(self):
        similars_node = []
        for node_class, node in self.parent.scene.items():
            if self._class_name not in node_class:
                continue
            similars_node.append(node)
        return similars_node


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
    # TODO if multiple same Class node (check with name)
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
