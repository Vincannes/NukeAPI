#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import json
from knob import Knob
import regex_wrapper as regw
from collections import OrderedDict

NODES_KNOBS = {}
path_node_knobs = os.path.join(os.path.dirname(__file__), "nodes_knobs.json")
with open(path_node_knobs, 'r') as json_path:
    NODES_KNOBS = json.load(json_path)


class Node(object):
    X_OFFSET = 0
    Y_OFFSET = 50
    DEFAULT_KNOBS = ["name", "inputs", "xpos", "ypos"]

    def __init__(self, class_name, parent):

        self.parent = parent

        self._class_name = class_name
        self._knobs_dict = {}
        self._knobs_object = {}

        if class_name == "Root":
            self._knobs_dict["inputs"] = 0
            self._knobs_object["inputs"] = 0
        else:
            self._set_default_knobs()

        self._sub_class_name = f"[{self._get_index()}]{class_name}"

    def name(self):
        return self._knobs_dict.get("name")

    def knob(self, knob_name):
        if knob_name not in self._knobs_object and \
                knob_name in NODES_KNOBS.get(self._class_name):
            self._knobs_dict[knob_name] = 0
            self._knobs_object[knob_name] = Knob(knob_name, parent=self)
        return self._knobs_object.get(knob_name)

    def Class(self):
        return self._class_name

    def subClass(self):
        return self._sub_class_name

    def isSelected(self):
        return self._knobs_dict.get("selected", False)

    def setXYPos(self, x, y):
        self._knobs_dict["xpos"] = x
        self._knobs_dict["ypos"] = y
        self._update_dict()

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

    def setSelected(self, selected=True):
        if selected:
            self._knobs_dict["selected"] = selected
        else:
            self._knobs_dict.pop("selected")

    def get_node_dict(self):
        return self._knobs_dict

    def xpos(self):
        return self._knobs_dict.get("xpos")

    def ypos(self):
        return self._knobs_dict.get("ypos")

    def build_node_from_data(self, data):
        for _knob_name, value in data.items():
            _knob = Knob(_knob_name, parent=self)
            _knob.setValue(value)
            self._knobs_dict[_knob_name] = value
            self._knobs_object[_knob_name] = _knob


    # PRIVATES

    def _update_dict(self):
        self.parent.scene[self._sub_class_name] = self._knobs_dict

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
            _int = regw.get_int_from_string(_name)
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

    def _set_default_knobs(self):
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


if __name__ == '__main__':
    from pprint import pprint
    pprint(NODES_KNOBS)