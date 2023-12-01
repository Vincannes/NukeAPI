#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re


def get_int_from_string(name):
    return int(re.search(r'(\d+)', name).group(1))


def refine_class_node(node):
    return re.sub(r'\[\d+\]', '', node)


def get_knob_and_value(line):
    return re.match(r'\s*([a-zA-Z0-9_]+)\s*([^\n]+)?', line)


def get_node_with_knobs(file_content):
    return re.findall(r'([a-zA-Z0-9_]+)\s*{([^}]*)}', file_content)
