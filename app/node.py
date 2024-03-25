#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re
import json
from pprint import pprint
from collections import OrderedDict

from knob import Knob

NODES_KNOBS = {}
path_node_knobs = os.path.join(os.path.dirname(__file__), "nodes_knobs.json")
with open(path_node_knobs, 'r') as json_path:
    NODES_KNOBS = json.load(json_path)


def get_int_from_string(name):
    match = re.search(r'(\d+)', str(name))
    if not re.search(r'(\d+)', str(name)):
        return 0
    return int(match.group(1))


class Node(object):
    X_OFFSET = 0
    Y_OFFSET = 50
    DEFAULT_KNOBS = ["name", "inputs", "xpos", "ypos"]
    SKIPS_KNOBS = ["nodes"]

    def __init__(self, class_name, parent):

        self.object = None
        self.parent = parent

        self._class_name = class_name
        self._knobs_dict = {}
        self._knobs_object = {}
        self._group_nodes = []
        self._dependencies = []
        self._parent_node = None

        if class_name == "Root":
            self._knobs_dict["inputs"] = 0
            self._knobs_object["inputs"] = 0
        else:
            self._set_default_knobs()

        self._sub_class_name = "[{}]{}".format(self._get_index(),class_name)

    @property
    def group_nodes(self):
        return self._group_nodes

    @property
    def parent_node(self):
        return self._parent_node

    def name(self):
        return self._knobs_dict.get("name")

    def begin(self):
        pass

    def end(self):
        pass

    def knob(self, knob_name):
        if knob_name not in self._knobs_object and \
                knob_name in NODES_KNOBS.get(self._class_name):
            self._knobs_dict[knob_name] = 0
            self._knobs_object[knob_name] = Knob(knob_name, parent=self)
        return self._knobs_object.get(knob_name)

    def knobs(self):
        return [knob for knob in self._knobs_object.values()]

    def Class(self):
        return self._class_name

    def subClass(self):
        return self._sub_class_name

    def dependent(self):
        """Nodes connected to this node
        """
        # pprint(self.parent.)
        pass

    def dependencies(self):
        """Nodes that this Node is connected to
        """
        pass

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

    def set_group_nodes(self, nodes=None):
        if nodes is None:
            nodes = []
        self._group_nodes = nodes

    def set_parent_node(self, node=None):
        self._parent_node = node

    def get_node_dict(self):
        return self._knobs_dict

    def xpos(self):
        return self._knobs_dict.get("xpos")

    def ypos(self):
        return self._knobs_dict.get("ypos")

    def build_node_from_data(self, data):
        for _knob_name, value in data.items():
            if _knob_name in self.SKIPS_KNOBS:
                continue
            if _knob_name == "addUserKnob":
                for _sub_knob in value:
                    _knob_name = _sub_knob.get("name")
                    _value = _sub_knob.get("value")

                    _knob = Knob(_knob_name, parent=self)
                    _knob.setValue(_value)
                    _knob.index_data = _sub_knob.get("index_knob")

                    self._knobs_dict[_knob_name] = _value
                    self._knobs_object[_knob_name] = _knob
            else:
                _knob = Knob(_knob_name, parent=self)
                _knob.setValue(value)
                self._knobs_dict[_knob_name] = value
                self._knobs_object[_knob_name] = _knob

    def add_dependencies(self, dependencies=None):
        if not dependencies:
            dependencies = []

        self._dependencies = dependencies

    def __str__(self):
        return "{} : {} '{}'".format(
            self.__class__, self._class_name, self._knobs_dict.get("name")#, ["{}: {}".format(i, j) for i, j in self._knobs_dict.items()]
        )

    # PRIVATES

    def _update_dict(self):
        self.parent.scene[self._sub_class_name] = self._knobs_dict

    def _get_positions(self):
        xpos = 0
        ypos = 0
        for node_data in self.parent.scene:
            for node_name, knobs in node_data.items():
                if node_name in self.parent.SKIP_NODES_TYPE or knobs.get("Class") in self.parent.SKIP_NODES_TYPE:
                    continue
                _xpos = knobs.get("xpos", 0)
                _ypos = knobs.get("ypos", 0)
                xpos += int(_xpos) + self.X_OFFSET
                ypos += int(_ypos) + self.Y_OFFSET
        return xpos, ypos

    def _get_index(self):
        return len(self._get_nodes_from_scene())

    def _generate_name(self):
        names_iter = [0]
        for _name in self._get_nodes_from_scene():
            _int = get_int_from_string(_name)
            names_iter.append(_int)
        index_name = max(names_iter) + 1
        return self._class_name + str(index_name)

    def _get_nodes_from_scene(self):
        similars_node = []
        for node_data in self.parent.scene:
            for node_name, knobs in node_data.items():
                if node_name in self.parent.SKIP_NODES_TYPE:
                    continue
                class_node = knobs.get("Class")
                if class_node != self._class_name:
                    continue
                similars_node.append(node_name)
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