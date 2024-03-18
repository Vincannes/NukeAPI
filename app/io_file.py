#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re
import json
from pprint import pprint


class SceneDict(object):

    def __init__(self, scene_path):
        self._errors = {}
        with open(scene_path, "r") as path_file:
            scene_text = path_file.read()

        self._scene_lines = scene_text.split("\n")
        self._group_nodes = self._get_group_nodes(self._scene_lines)
        self._group_nodes_filtered = self._filtrer_ranges(self._group_nodes)
        self._orig_dict = self._scene_to_dict()
        self._dict_scene = self._orig_dict
        self._inputs_nodes = self._get_all_inputs()

    @property
    def errors(self):
        return self._errors

    def groups(self, filtered=True):
        return self._group_nodes if not filtered else self._group_nodes_filtered

    def get_dict(self):
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

    # Scene to Dict

    def _scene_to_dict(self):
        """Parse each group of nodes into dict
        result = {NodeClass: {
                IndexNode: [string of knobs],
                IndexNode: [string of knobs]
            }
        }
        return: Dict
        {NodeClass: {
                NodeName: {knobs; values},
                NodeName: {knobs; values},
            }
        }
        """
        result_node_list = {}

        for num_ligne, end_ligne in sorted(self._group_nodes_filtered.items()):
            node_class = self._scene_lines[num_ligne].split(" ")[0]

            if node_class == "version":
                result_node_list[node_class] = {}
                result_node_list[node_class][1] = self._scene_lines[num_ligne]
                continue

            elif node_class == "add_layer":
                if not node_class in result_node_list.keys():
                    result_node_list[node_class] = {}
                result_node_list[node_class][num_ligne] = self._scene_lines[num_ligne]
                continue

            if node_class not in result_node_list.keys():
                result_node_list[node_class] = {}
                index = 1
            else:
                index = max(result_node_list[node_class].keys()) + 1

            result_node_list[node_class][index] = []

            for i_range in range(num_ligne, end_ligne - 1):
                ligne = self._scene_lines[i_range]
                index = max(result_node_list[node_class].keys())
                result_node_list[node_class][index].append(ligne)

        result = self._knobs_from_data(result_node_list)
        return result

    def _knobs_from_data(self, list_nodes):
        """Parse each Node with the list of his strings
        {NodeClass: {
                NodeName: {knobs},
                NodeName: {knobs},
            }
        }
        """
        result = {}
        for node_class, data in list_nodes.items():
            for index, lines in data.items():
                if node_class in ["Root", "define_window_layout_xml"]:
                    result[node_class] = self._parse_knobs_for_node(lines)
                elif node_class == "version":
                    result[node_class] = lines.split(" ", 1)[-1]
                elif node_class == "add_layer":
                    layer_node = self._get_next_nodes_from_line(index)
                    layer = {"value": lines.replace("{", "").replace("}", "")}
                    if node_class not in result.keys():
                        result[node_class] = {}
                    if not layer_node in result[node_class].keys():
                        result[node_class][layer_node] = []
                    result[node_class][layer_node].append(layer)
                else:
                    datas = self._parse_knobs_for_node(lines)
                    if not node_class in result.keys():
                        result[node_class] = {}
                    result[node_class][datas.get('name')] = self._parse_knobs_for_node(lines)
        return result

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

                if isinstance(result[knob], str):
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
                    splited = line.split(' ')
                    knob, value = splited[0], splited[-1]
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
                    out_range = _out + 1

        if in_range is not None:
            for _in, _out in self._group_nodes_filtered.items():
                if _in <= in_range <= _out:
                    in_range = _in

        if not in_range and not out_range:
            return None, None

        cles_in = list(self._group_nodes_filtered.keys())
        cles_out = list(self._group_nodes_filtered.values())

        if in_range and not in_range in cles_in or out_range and out_range not in cles_out:
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
            if "name" not in ligne:
                continue
            name = ligne.split(" ")[-1]
        return name

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
        groups_out = list(self._group_nodes_filtered.values())

        index_2 = 1
        for i, ligne in enumerate(self._scene_lines, 0):

            if ligne.startswith("set "):
                node_object = ligne.split(" ")[1]
                if node_object == "cut_paste_input":
                    continue
                if self._scene_lines[i-1] == "end_group":
                    i += 1
                node_name = self._get_name(out_range=i)
                _inputs_nodes[node_name] = {
                    "name": node_name,
                    "object": node_object,
                    "dependents": []
                }

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

                node_name_from_object = [a for a in _inputs_nodes.values() if a.get("object") == node_object_input]
                if not node_name_from_object:
                    continue
                _inputs_nodes[node_name_from_object[0].get("name")]["dependents"].append(node_name)

            # Multiples Inputs
            elif re.match(r" inputs (?!0$)[12]$", ligne):
                #Si tous les nodes au dessus ont pas de inputs alors
                #Le node
                #TODO if node is not above above have to find the right node
                in_range = [in_range for in_range, out_range in self._group_nodes_filtered.items() if in_range <= i <= out_range][0]
                node_name = self._get_name(in_range=in_range)
                index_cle_in = groups_in.index(in_range)
                group_above_in = groups_in[index_cle_in - 1]
                node_above_name = self._get_name(in_range=group_above_in)

                _multi_inputs_nodes[in_range] = [node_name, node_above_name]
                index_2 += 1

                if node_name in _inputs_nodes.keys():
                    _inputs_nodes[node_name]["dependents"].append(node_above_name)
                else:
                    _inputs_nodes[node_name] = {
                        "name": node_name,
                        "dependents": [node_above_name]
                    }

        # If Group has no "inputs 0" get Input node above him
        for i, (in_range, out_range) in enumerate(self._group_nodes_filtered.items()):
            has_input = True
            node_name = self._get_name(in_range)

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
                node_above_name = self._get_name(in_range=group_above_in)
                if node_above_name not in _inputs_nodes.keys():
                    _inputs_nodes[node_above_name] = {}
                    _inputs_nodes[node_above_name] = {
                        "dependents": [node_name],
                        "name": node_above_name,
                        "object": None
                    }
                else:
                    _inputs_nodes[node_above_name]["dependents"].append(node_name)

        _nodes_already_use = []
        for in_range, (node, f_input_node) in _multi_inputs_nodes.items():
            s_input_node = None
            for i in reversed(range(in_range)):
                ligne = self._scene_lines[i]
                if ligne.startswith("push"):
                    node_name = self._get_name(out_range=i-1)
                    if not node_name in _nodes_already_use:
                        _nodes_already_use.append(node_name)
                        s_input_node = node_name
                        break

            if not node in _inputs_nodes.keys():
                _inputs_nodes[node] = {
                    "dependents": [f_input_node, s_input_node],
                    "name": node,
                    "object": None
                }
            else:
                _inputs_nodes[node]["dependents"].append(s_input_node)

        return _inputs_nodes

    def _get_next_nodes_from_line(self, line):
        node_name = None
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
    path_test_file = "D:\\Desk\\python\\NukeAPI\\tests\\083_060-cmp-base-v016.nk"
    result_dict = SceneDict(path_test_file)
    pprint(result_dict.get_dict().get("add_layer"))
    # pprint(result_dict.groups())
    # pprint(result_dict.groups(False))
