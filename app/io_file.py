#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re
import json
from pprint import pprint


class SceneDict(object):

    SPECIALS_NODES_KEYS = ["Root", "define_window_layout_xml", "version", "add_layer", "clone"]

    def __init__(self, scene_path):
        self._errors = {}
        with open(scene_path, "r") as path_file:
            scene_text = path_file.read()

        self._scene_lines = scene_text.split("\n")
        self._len_lines = len(self._scene_lines)
        self._group_nodes = self._get_group_nodes(self._scene_lines)
        self._group_nodes_filtered = self._filtrer_ranges(self._group_nodes)
        self._inputs_nodes = self._get_all_inputs()
        self._orig_dict = self._scene_to_dict()
        self._dict_scene = self._orig_dict

    @property
    def errors(self):
        return self._errors

    @property
    def index_groups(self, filtered=True):
        return self._group_nodes if not filtered else self._group_nodes_filtered

    def get_nodes(self):
        return self._dict_scene

    def get_inputs(self):
        return self._inputs_nodes

    def update_dict(self, dictionary):
        self._dict_scene = dictionary

    def dict_to_scene(self, path):
        return self._dict_to_scene(path)

    def export_to_file(self, path):
        json_object = json.dumps(self._dict_scene, indent=4)
        with open(path, "w") as outfile:
            outfile.write(json_object)

    # PRIVATES

    def _get_class_node_by_key(self, _liste, node_class):
        nodes_class = []
        index = None
        for i, dictionnaire in enumerate(_liste):
            if node_class in dictionnaire.keys():
                nodes_class.append(dictionnaire[node_class])
                index = i
        return index, nodes_class

    # Scene to Dict

    def _scene_to_dict(self):
        result = []
        _group_name = (None, None)
        for num_ligne, end_ligne in sorted(self._group_nodes_filtered.items()):
            node_class = self._scene_lines[num_ligne].split(" ")[0]

            lines = []
            if num_ligne == end_ligne:
                lines.append(self._scene_lines[num_ligne])
            else:
                for i_range in range(num_ligne, end_ligne):
                    lines.append(self._scene_lines[i_range])

            if node_class == "version":
                _version = {"version": {"version": lines[0].split(" ", 1)[-1]}}
                result.append(_version)
                continue

            elif node_class == "define_window_layout_xml": # ici perte data pour window "Root", 
                result.append({node_class: {node_class: lines}})

            elif node_class == "Root":
                result.append({node_class: self._parse_knobs_for_node(lines)})

            elif node_class == "add_layer":
                layer_node = self._get_next_node_from_line(num_ligne)
                layer = lines[0].replace("{", "").replace("}", "")
                node_index, class_node = self._get_class_node_by_key(result, node_class)
                if not class_node:
                    result.append({node_class: {layer_node: [layer]}})
                else:
                    add_layers = result[node_index][node_class]
                    if not layer_node in add_layers.keys():
                        result[node_index][node_class][layer_node] = [layer]
                    else:
                        result[node_index][node_class][layer_node].append(layer)

            elif node_class == "clone":
                node_object = self._scene_lines[num_ligne].split(" ")[1].replace("$", "")

                node = next((
                    node for scene, nodes in self._inputs_nodes.items() for node in nodes for node_name, _data in node.items() if _data.get("object") == node_object
                ))
                node_name = next(i.get("name") for i in node.values())

                _data = self._parse_knobs_for_node(lines)
                _data["clone_name"] = node_name
                _data["clone_object"] = node_object

                node_index, class_node = self._get_class_node_by_key(result, node_class)
                if not node_index:
                    result.append({node_class: [{node_name: _data}]})
                else:
                    result[node_index][node_class].append({node_name: _data})

            elif node_class in ["Group", "Gizmo"]:
                _data = self._parse_knobs_for_node(lines)
                grp_name = _data.get("name")
                _data["Class"] = node_class
                _data["nodes"] = []
                _group_name = (node_class, grp_name)
                result.append({grp_name: _data})

            # Dans un GROUP
            elif _group_name[0] is not None:
                if any([self._scene_lines[num_ligne-i] == "end_group" for i in range(0, 6)]):
                    _group_name = (None, None)
                    continue
                _data = self._parse_knobs_for_node(lines)
                _data["Class"] = node_class
                sub_node_name = _data.get("name")
                group_index, group = self._get_class_node_by_key(result, _group_name[1])
                result[group_index][_group_name[1]]["nodes"].append({sub_node_name: _data})

            else:
                _data = self._parse_knobs_for_node(lines)
                _data["Class"] = node_class
                node_name = _data.get("name")
                result.append({node_name: _data})

        return result

    def _get_groups_nodes(self, result_dict):
        _is_group = False
        _group_name = None
        for i, line in enumerate(self._scene_lines):
            if line.startswith("Group"):
                _is_group = True
                _group_name = self._get_name(in_range=i)
                result_dict["Group"][_group_name]["nodes"] = []
            elif line.startswith("end_group") and _is_group:
                _is_group = False
                _group_name = None
            if not _is_group:
                continue
            if any([self._scene_lines[i].startswith(a) for a in ["set", "push"]]):
                continue
            curr_node_name = self._get_name(in_range=i)
            if _is_group and curr_node_name != _group_name:
                if curr_node_name not in result_dict["Group"][_group_name]["nodes"]:
                    result_dict["Group"][_group_name]["nodes"].append(curr_node_name)
        return result_dict

    def _parse_knobs_for_node(self, lines):
        """Parse each line of Node string list
        {knob: value,
         knob: [values]
        }
        :param lines:
        """
        result = {}
        prev_knob = None
        knob_class = None
        for i, line in enumerate(lines):

            if i == 0:
                knob_class = line.split(" ")[0]
                continue

            custom_knobs = re.findall(r"([a-zA-Z0-9]+) \{(.+?)\}", line)
            space_data = re.match(r"^(\s+)\{(.*)$", line)

            # if same knob with more datas
            if len(custom_knobs) > 0:
                knob, value = custom_knobs[0][0], custom_knobs[0][1]
                if knob not in result.keys():
                    result[knob] = []

                if knob == "addUserKnob":
                    splited = value.split(" ")
                    _user_knob = {
                        "name": splited[1],
                        "index_knob": splited[0],
                        "value": " ".join(splited[2:])
                        
                    }
                    result[knob].append(_user_knob)
                    continue

                elif isinstance(result[knob], str):
                    tmp_val = result[knob]
                    del result[knob]
                    result[knob] = []
                    result[knob].append(tmp_val)

                result[knob].append(value)
                prev_knob = None

            # if space with some datas
            elif space_data:
                if not prev_knob:
                    prev_knob = lines[i - 1].split(" ")[0]
                if prev_knob not in result.keys():
                    result[prev_knob] = []

                if isinstance(result[prev_knob], str):
                    tmp_val = result[prev_knob]
                    del result[prev_knob]
                    result[prev_knob] = []
                    result[prev_knob].append(tmp_val)

                result[prev_knob].append(line)



            # is space or empty line
            elif len(re.findall(r"^\s*$", line)) > 0:
                continue

            # is only { or }
            elif any(a in line for a in ["{", "}"]):
                if not "knob" in result.keys():
                    result["knob"] = []
                result["knob"].append(line)

            # normal knob
            else:
                try:
                    if line[0] == " ":
                        line = line[1:]
                    splited = line.split(' ')
                    knob, value = splited[0], " ".join(splited[1:]).replace('"', "")
                    result[knob] = value
                    prev_knob = None
                except:
                    if knob_class not in self._errors.keys():
                        self._errors[knob_class] = []
                    self._errors[knob_class].append((i, line))
        return result

    def _filtrer_ranges(self, dictionnary):
        """Remove ranges that are already inside a range.
        [(10, 15), (11, 12), (15, 20)] => [(10, 15), (15, 20)]
        :param dictionnaire:
        :return:
        """
        resultats = {}
        ranges_traites = []

        for cle, valeur in sorted(dictionnary.items()):
            inclut = False

            for range_trait in ranges_traites:
                if cle >= range_trait[0] and valeur <= range_trait[1]:
                    inclut = True
                    break

            if not inclut:
                resultats[cle] = valeur
                ranges_traites.append((cle, valeur))

        return resultats

    def _get_group_nodes(self, lines):
        """Get group of stacks of { }
        :param lines:
        :return: list of tuple
        """
        pile = []
        group_nodes = {}
        for num_ligne, ligne in enumerate(lines, start=0):
            for i, caractere in enumerate(ligne, start=0):
                if caractere == '{':
                    pile.append(num_ligne)
                elif caractere == '}':
                    if pile:
                        accolade_ouverte = pile.pop()
                        accolade_fermante = num_ligne
                        group_nodes[accolade_ouverte] = accolade_fermante
                elif "version" in ligne:
                    group_nodes[num_ligne] = num_ligne
        return group_nodes

    def _get_group_from_ligne(self, in_range=None, out_range=None):
        if in_range is not None and in_range == 0 or out_range is not None and out_range == 0:
            return None, None

        if out_range is not None:
            for _in, _out in self._group_nodes_filtered.items():
                if _in <= out_range <= _out:
                    in_range = _in
                    out_range = _out
                    break
        if in_range is not None:
            for _in, _out in self._group_nodes_filtered.items():
                if _in <= in_range <= _out:
                    in_range = _in
                    out_range = _out
                    break

        if not in_range and not out_range:
            return None, None

        cles_in = list(self._group_nodes_filtered.keys())
        cles_out = list(self._group_nodes_filtered.values())

        if in_range and in_range not in cles_in or out_range and out_range not in cles_out:
            return None, None

        index_cle = cles_in.index(in_range) if in_range else cles_out.index(out_range-1)

        if out_range:
            in_range = cles_in[index_cle]
        elif in_range:
            out_range = cles_out[index_cle]

        return in_range, out_range

    def _get_name(self, in_range=None, out_range=None):
        name = "NoneName"
        in_range, out_range = self._get_group_from_ligne(in_range, out_range)

        if in_range is None and out_range is None:
            return name

        for ligne_index in range(in_range, out_range):
            ligne = self._scene_lines[ligne_index]
            if not re.match(r"\s*name", ligne):
                continue
            name = ligne.split(" ")[-1]
        return name

    def _get_class(self, in_range=None, out_range=None):
        name = None
        in_range, out_range = self._get_group_from_ligne(in_range, out_range)

        if in_range is None and out_range is None:
            return name

        class_name = self._scene_lines[in_range].split(" ")[0]
        return class_name

    def _get_class_name_node(self, index):
        node_name = self._get_name(out_range=index)
        class_name = self._get_class(out_range=index)
        if node_name == "NoneName":
            while True:
                index -= 1
                node_name = self._get_name(out_range=index)
                class_name = self._get_class(out_range=index)
                if node_name != "NoneName":
                    break
        return class_name, node_name

    def _get_all_inputs(self):
        """
        set = set to group above a Node Object
        push = connect group bellow to Node Object

        node['dependents'] = nodes qui ont pour input ce node, ou tous les nodes
                             connecte a ce node. Node Bellow
        :return:
        """
        _inputs_nodes = {}
        _multi_inputs_nodes = {}
        groups_in = list(self._group_nodes_filtered.keys())

        curr_scene_name = "current_scene"
        for i, ligne in enumerate(self._scene_lines, 0):

            # IS GROUP PART
            if any([self._scene_lines[i].startswith(a) for a in ["Group", "Gizmo", "LiveGroup"]]):
                curr_scene_name = self._get_name(in_range=i)
            elif self._scene_lines[i] == "end_group":
                curr_scene_name = "current_scene"

            if ligne.startswith("set "):
                node_object = ligne.split(" ")[1]
                if node_object == "cut_paste_input":
                    continue

                node_name = self._get_name(out_range=i)
                if node_name == "NoneName":
                    ri = i
                    while True:
                        ri -= 1
                        if ri < 0:
                            break
                        node_name = self._get_name(out_range=ri)
                        if node_name != "NoneName":
                            break

                if not curr_scene_name in _inputs_nodes.keys():
                    _inputs_nodes[curr_scene_name] = []

                _inputs_nodes[curr_scene_name].append({node_name: {
                    "name": node_name,
                    "object": node_object,
                    "dependents": []
                }})

            elif ligne.startswith("push "):
                _object_node = ligne.split(" ")[1]
                if not _object_node.startswith("$"):
                    continue
                node_object_input = _object_node.replace("$", "")

                index_class = i
                while True:
                    if not self._scene_lines[index_class].startswith("push"):
                        break
                    index_class += 1
                node_name = self._get_name(in_range=index_class)
                node_name_from_object = [
                    r for a in _inputs_nodes[curr_scene_name] for r in a.values() if r.get("object") == node_object_input
                ]
                if not node_name_from_object:
                    continue
                parent_node_name = node_name_from_object[0].get("name")
                index_node, parent_node = self._get_class_node_by_key(_inputs_nodes[curr_scene_name], parent_node_name)
                _inputs_nodes[curr_scene_name][index_node].get(parent_node_name)["dependents"].append(node_name)

            # Multiples Inputs
            #TODO calculat inputs number and get above from this number
            elif re.match(r"inputs (?!0$)[12]$", ligne):
                in_range = [in_range for in_range, out_range in self._group_nodes_filtered.items() if in_range <= i <= out_range][0]
                node_name = self._get_name(in_range=in_range)
                index_cle_in = groups_in.index(in_range)
                group_above_in = groups_in[index_cle_in - 1]
                node_above_name = self._get_name(in_range=group_above_in)

                if not curr_scene_name in _inputs_nodes.keys():
                    _node = {node_above_name: {
                        "name": node_above_name,
                        "dependents": [node_name]
                    }}
                    _inputs_nodes[curr_scene_name] = [_node]
                else:
                    index_node, node = self._get_class_node_by_key(_inputs_nodes[curr_scene_name], node_above_name)
                    if not index_node:
                        _inputs_nodes[curr_scene_name].append({
                            node_above_name: {
                                "name": node_above_name,
                                "dependents": [node_name]
                            }
                        })
                    else:
                        _inputs_nodes[curr_scene_name][index_node].get(node_above_name)["dependents"].append(node_name)

        # If Group has no "inputs 0" get Input node above him
        for i, (in_range, out_range) in enumerate(self._group_nodes_filtered.items()):

            # IS GROUP PART
            if any([self._scene_lines[in_range].startswith(a) for a in ["Group", "Gizmo", "LiveGroup"]]):
                curr_scene_name = self._get_name(in_range=in_range)
            elif any([self._scene_lines[in_range - _i] == "end_group" for _i in range(0, 6)]):
                curr_scene_name = "current_scene"

            if not curr_scene_name in _inputs_nodes.keys():
                _inputs_nodes[curr_scene_name] = []

            has_input = True
            node_name = self._get_name(in_range=in_range)
            for ligne_index in range(in_range, out_range):
                ligne = self._scene_lines[ligne_index]
                if "inputs 0" in ligne:
                    has_input = False
                    break

            if has_input:
                if node_name == "NoneName":
                    continue
                index_cle_in = groups_in.index(in_range)
                group_above_in = groups_in[index_cle_in - 1]
                if self._scene_lines[in_range-2] == "end_group":
                    while True:
                        group_above_in -= 1
                        if self._scene_lines[group_above_in].startswith("Group"):
                            break
                node_above_name = self._get_name(in_range=group_above_in)
                if node_above_name == "NoneName":
                    while True:
                        group_above_in -= 1
                        node_above_name = self._get_name(in_range=group_above_in)
                        if node_above_name != "NoneName":
                            break

                if node_above_name not in _inputs_nodes[curr_scene_name]:
                    _inputs_nodes[curr_scene_name].append({node_above_name: {
                        "dependents": [node_name],
                        "name": node_above_name,
                        "object": None
                    }})
                else:
                    sub_node_index, _ = self._get_class_node_by_key(_inputs_nodes[curr_scene_name], node_above_name)
                    _inputs_nodes[curr_scene_name][sub_node_index].get(node_above_name)["dependents"].append(node_name)

        _nodes_already_use = []
        for in_range, (node, f_input_node) in _multi_inputs_nodes.items():

            # IS GROUP PART
            if any([self._scene_lines[in_range].startswith(a) for a in ["Group", "Gizmo", "LiveGroup"]]):
                curr_scene_name = self._get_name(in_range=in_range)
            elif any([self._scene_lines[in_range - _i] == "end_group" for _i in range(0, 6)]):
                curr_scene_name = "current_scene"

            s_input_node = None
            for i in reversed(range(in_range)):
                ligne = self._scene_lines[i]
                if ligne.startswith("push"):
                    node_name = self._get_name(out_range=i-1)
                    if not node_name in _nodes_already_use:
                        _nodes_already_use.append(node_name)
                        s_input_node = node_name
                        break

            if not node in _inputs_nodes[curr_scene_name]:
                _inputs_nodes[curr_scene_name].append({node: {
                    "dependents": [f_input_node, s_input_node],
                    "name": node,
                    "object": None
                }})
            else:
                node_index, _ = self._get_class_node_by_key(_inputs_nodes[curr_scene_name], node)
                _inputs_nodes[curr_scene_name][node_index].get(node)["dependents"].append(node)

        return _inputs_nodes

    def _get_next_node_from_line(self, line):
        while True:
            curr_line = self._scene_lines[line]
            if any([True for a in ["add_layer"] if a in curr_line]):
                line += 1
            elif curr_line:
                node_name = self._get_name(in_range=line)
                break
        return node_name

    # Dict to Scene

    def _dict_to_scene(self, file_out):
        with open(file_out, 'w') as file:
            output = ""
            output += "version {}\n".format(self._dict_scene.get('version'))

            output += "Root {"
            for root_knob, value in self._dict_scene.get("Root").items():
                output += "{} {}\n".format(root_knob, value)

            output += "}\n"

            for node_class, nodes in self._dict_scene.items():
                if node_class in ["version", "define_window_layout_xml", "Root"]:
                    continue
                for node_name, knobs_data in nodes.items():
                    output += node_class + " {\n"

                    for knob, value in knobs_data.items():
                        if isinstance(value, list):
                            for i, val in enumerate(value):
                                if i == 0:
                                    val = knob + " " + val
                                output += val +" \n"
                        else:
                            output += "{} {}\n".format(knob, value)
                    output += "}\n"

            file.write(output)
        return output


if __name__ == "__main__":
    import os
    this_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_out = os.path.join(os.path.dirname(this_dir), "tests", "test_final_2.nk")
    path_test_file = os.path.join(os.path.dirname(this_dir), "tests", "083_060-cmp-base-v016.nk")
    path_test_file ="/homes/trolardv/Documents/0089_mou_0010-vzero-base-v003.nk"
    result_dict = SceneDict(path_test_file)
    # pprint(result_dict.get_dict().get("Group").get("ColourDilate_FS2"))
    # pprint(result_dict.get_nodes().get("Group")))
    # pprint(result_dict.get_nodes())
    # pprint([i for i in result_dict.get_nodes() if i.get("Group")])
    # for i in result_dict.get_nodes():
    #     for name, data in i.items():
    #         print(data)
    #         print(data.get("Class"))
    pprint([data for i in result_dict.get_inputs().get("current_scene") for name, data in i.items() if data.get("name") == "Dot_Retime"])
    # pprint([data for i in result_dict.get_nodes() for name, data in i.items() if isinstance(data, dict) and data.get("Class") == "Group"])
    # pprint([data for i in result_dict.get_nodes() for name, data in i.items() if name == "version"])
    # pprint(result_dict.get_inputs())
    print("")
    # pprint(result_dict.get_inputs())
    # pprint(result_dict.get_dict().get("Group").keys())
    # pprint(result_dict.get_inputs().get("NoneName"))
    # pprint(result_dict.groups(False))
