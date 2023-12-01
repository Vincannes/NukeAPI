#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re

from pprint import pprint
import io_file

test_file = "D:\\Desk\\python\\NukeAPI\\tests\\test.nk"
test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final.nk"

with open(test_file, 'r') as file:
    file_content = file.read()

parsed_data = io_file.nk_scene_to_dict(file_content)
pprint(parsed_data)
io_file.dict_to_nk_scene(parsed_data, test_file_out)

