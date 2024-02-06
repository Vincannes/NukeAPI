#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from pprint import pprint
import regex_wrapper as regw


def parse_node_group(node_group):
    node_info = {}
    for line in node_group.split('\n'):
        match = regw.get_knob_and_value(line)
        if match:
            key, value = match.groups()
            if value:
                node_info[key] = value.strip()
            else:
                node_info[key] = None
    return node_info


def nk_scene_to_dict(file_content):
    node_groups = regw.get_node_with_knobs(file_content)
    parsed_data = {}
    pprint(node_groups)
    for node_name, node_group_content in node_groups:
        if node_name.strip() in ["define_window_layout_xml"]:
            continue
        parsed_data[node_name.strip()] = parse_node_group(node_group_content)

    return parsed_data


def dict_to_nk_scene(scene_dict, file_out):
    with open(file_out, 'w') as file:
        for node, values in scene_dict.items():
            _node = regw.refine_class_node(node) + " {\n"
            file.write(_node)
            for knob, value in values.items():
                _value = f" {knob} {value}\n"
                file.write(_value)
            out_node = "}\n"
            file.write(out_node)
