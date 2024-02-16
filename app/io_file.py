#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re
import json
from pprint import pprint


class SceneParser(object):

    def __init__(self, scene_text):
        self._errors = {}
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
                    knob, value = splited[1], splited[2]
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
                    out_range = _out+1

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

    # Dict to Scene

    def _dict_to_scene(self, file_out):
        with open(file_out, 'w') as file:
            output = ""
            output += f"version {self._dict_scene.get('version')}\n"

            output += "Root {"
            for root_knob, value in self._dict_scene.get("Root").items():
                output += f"{root_knob} {value}\n"

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
                            output += f"{knob} {value}\n"
                    output += "}\n"

            file.write(output)
        return output


if __name__ == "__main__":
    input_string = """
#! /s/apps/packages/cg/nuke/13.2.v8/platform-linux/libnuke-13.2.8.so -nx
#write_info out file:"/s/prods/sharks/sequence/083/083_060/cmp/image/wip/083_060-cmp-base-nk-out-v016-aces-exr/083_060-cmp-base-nk-out-v016-aces.%04d.exr" format:"3840 2160 1" chans:":rgba.red:rgba.green:rgba.blue:" framerange:"991 1062" fps:"0" colorspace:"aces" datatype:"16 bit half" transfer:"unknown" views:"main" colorManagement:"OCIO"
version 13.2 v8
define_window_layout_xml {<?xml version="1.0" encoding="UTF-8"?>
<layout version="1.0">
    <window x="0" y="31" w="1920" h="1025" maximized="1" screen="1">
        <splitter orientation="1">
            <split size="40"/>
            <dock id="" hideTitles="1" activePageId="Toolbar.1">
                <page id="Toolbar.1"/>
            </dock>
            <split size="1257" stretch="1"/>
            <splitter orientation="2">
                <split size="986"/>
                <dock id="" activePageId="DAG.1">
                    <page id="DAG.1"/>
                    <page id="Curve Editor.1"/>
                    <page id="DopeSheet.1"/>
                </dock>
            </splitter>
            <split size="615"/>
            <splitter orientation="2">
                <split size="889"/>
                <dock id="" activePageId="Properties.1">
                    <page id="Properties.1"/>
                    <page id="uk.co.thefoundry.backgroundrenderview.1"/>
                </dock>
                <split size="93"/>
                <dock id="" activePageId="Pixel Analyzer.1">
                    <page id="Pixel Analyzer.1"/>
                </dock>
            </splitter>
        </splitter>
    </window>
    <window x="1920" y="0" w="1920" h="1176" maximized="1" screen="0">
        <splitter orientation="1">
            <split size="958"/>
            <dock id="" activePageId="Viewer.1">
                <page id="Viewer.1"/>
            </dock>
            <split size="958"/>
            <dock id="" activePageId="Viewer.2">
                <page id="Viewer.2"/>
            </dock>
        </splitter>
    </window>
</layout>
}
Root {
inputs 0
name /s/prods/sharks/sequence/083/083_060/cmp/nuke/wip/083_060-cmp-base-v016.nk
frame 1029
first_frame 991
last_frame 1062
logLut compositing_log
floatLut scene_linear
addUserKnob {20 mariTab l Mari}
addUserKnob {26 cmdStatus l "listen status" t "The status of Nuke's command port" T <b>Disabled</b>}
addUserKnob {26 sendStatus l "send status" t "The status of Nuke's connection to Mari" T <b>Inactive</b>}
addUserKnob {3 socketPortSend l port t "Port that Mari is listening to. Make sure this matches the command port set in Mari's preferences." -STARTLINE}
socketPortSend 6100
}
Reformat {
addUserKnob {20 studio l Studio}
inputs 0
name Reformat2
zzz qzdqzdqz
}
Reformat {
name Reformat1
}
Tracker4 {
tracks { { 1 31 1 } 
{ { 5 1 20 enable e 1 } 
{ 3 1 75 name name 1 } 
{ 2 1 58 track_x track_x 1 } 
{ 2 1 58 track_y track_y 1 } 
{ 2 1 63 offset_x offset_x 1 } 
{ 2 1 63 offset_y offset_y 1 } 
{ 4 1 27 T T 1 } 
{ 4 1 27 R R 1 } 
{ 4 1 27 S S 1 } 
{ 2 0 45 error error 1 } 
{ 1 1 0 error_min error_min 1 } 
{ 1 1 0 error_max error_max 1 } 
{ 1 1 0 pattern_x pattern_x 1 } 
{ 1 1 0 pattern_y pattern_y 1 } 
{ 1 1 0 pattern_r pattern_r 1 } 
{ 1 1 0 pattern_t pattern_t 1 } 
{ 1 1 0 search_x search_x 1 } 
{ 1 1 0 search_y search_y 1 } 
{ 1 1 0 search_r search_r 1 } 
{ 1 1 0 search_t search_t 1 } 
{ 2 1 0 key_track key_track 1 } 
{ 2 1 0 key_search_x key_search_x 1 } 
{ 2 1 0 key_search_y key_search_y 1 } 
{ 2 1 0 key_search_r key_search_r 1 } 
{ 2 1 0 key_search_t key_search_t 1 } 
{ 2 1 0 key_track_x key_track_x 1 } 
{ 2 1 0 key_track_y key_track_y 1 } 
{ 2 1 0 key_track_r key_track_r 1 } 
{ 2 1 0 key_track_t key_track_t 1 } 
{ 2 1 0 key_centre_offset_x key_centre_offset_x 1 } 
{ 2 1 0 key_centre_offset_y key_centre_offset_y 1 } 
} 
{ 
 { {curve K x1001 1} "track 1" {curve x1001 2224 2224.851074 2225.715332 2226.397705 2226.286865 2226.01123 2225.207275 2223.173828 2221.169434 2219.116211 2217.347412 2216.131592 2214.848145 2213.945801 2213.450684 2212.960205 2212.460693 2211.925293 2211.004883 2210.444092 2209.67041 2208.61499 2207.770996 2206.390137 2205.113037 2203.652344 2202.257324 2200.728027 2199.290283 2197.264893 2195.192871 2192.468994 2189.462158 2186.328369 2183.174072 2180.232422 2177.762939 2175.666016 2174.250732 2172.950439 2171.604492 2170.625732 2169.560547 2168.645996 2168.165283 2168.086914 2168.236816 2168.889893 2170.130615 2171.581299 2173.24585 2174.920654} {curve x1001 1860 1863.0354 1865.789795 1868.117798 1869.901611 1871.505127 1872.955078 1873.661865 1874.165283 1874.388184 1874.030884 1873.675293 1872.404785 1870.122192 1867.183472 1863.486816 1858.775024 1853.927002 1848.639893 1843.838135 1839.230469 1835.383545 1832.406128 1830.156494 1828.593872 1827.486328 1827.036011 1826.752686 1827.036499 1827.763306 1828.990601 1830.324463 1832.026733 1833.648438 1835.559814 1837.482178 1839.651367 1841.62561 1843.864258 1846.248535 1848.585327 1851.29834 1854.139404 1857.154053 1860.586304 1864.384644 1868.463623 1872.884033 1877.807251 1882.968384 1888.463257 1893.717896} {curve K x1001 0} {curve K x1001 0} 1 0 0 {curve x1001 0 0.0007891349869 0.0009463882028 0.0007646258149 0.00108984438 0.001076249483 0.001153578598 0.0009828207034 0.0009781733488 0.000711175286 0.00101161366 0.0007645238832 0.001503069177 0.0007349097129 0.0009024507132 0.00101141958 0.0007764981812 0.0006919009998 0.0008216288031 0.0006662888449 0.0009192168945 0.0006932919065 0.001320701837 0.0007720051607 0.001128956896 0.0008261216022 0.0008675200191 0.0006416602779 0.001007886543 0.0006697528675 0.0009834801212 0.0008107085937 0.0009680948175 0.0007011225898 0.001229174566 0.0008621634372 0.000777894517 0.0007262841365 0.0008511445097 0.0008173744826 0.001109491068 0.000915746988 0.001145127512 0.0007334602583 0.0009393520816 0.000605183796 0.001305977988 0.0006272291242 0.0007889151837 0.0007234922129 0.001071596619 0.0005567849194} 0 0.00150307 -72 -72 72 72 -50 -50 50 50 {curve} {curve x1001 2102} {curve x1001 1738} {curve x1001 2345} {curve x1001 1981} {curve x1001 2152} {curve x1001 1788} {curve x1001 2295} {curve x1001 1931} {curve x1001 71.5} {curve x1001 71.5}  } 
} 
}
name Tracker1
nadddd test
}
RotoPaint {
cliptype bbox
curves {{{v x3f99999a}
  {f 0}
  {n
   {layer Root
    {f 2097152}
    {t x44f00000 x44870000}
    {a pt1x 0 pt1y 0 pt2x 0 pt2y 0 pt3x 0 pt3y 0 pt4x 0 pt4y 0 ptex00 0 ptex01 0 ptex02 0 ptex03 0 ptex10 0 ptex11 0 ptex12 0 ptex13 0 ptex20 0 ptex21 0 ptex22 0 ptex23 0 ptex30 0 ptex31 0 ptex32 0 ptex33 0 ptof1x 0 ptof1y 0 ptof2x 0 ptof2y 0 ptof3x 0 ptof3y 0 ptof4x 0 ptof4y 0 pterr 0 ptrefset 0 ptmot x40800000 ptref 0}
    {cubiccurve Clone16 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44fd8000 x44980000 x3f0f6000}
       {x44fe8000 x449bc000 x3f2c6000}
       {x44fe8000 x449d0000 x3f2fa000}
       {x44fb8000 x44a60000 x3f396000}
       {x44fb0000 x44a68000 x3f412000}
       {x44fcc000 x44a1c000 x3f422000}
       {x44fe8000 x4499c000 x3f43e000}
       {x44fd4000 x44988000}}}
     {t x44fd3000 x449e2800}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x439c8000 bu 1 src 1 stx x41c00000 sty x43540000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}
    {cubiccurve Clone15 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44d38000 x44a0c000 x3e868000}
       {x44d24000 x44a4c000 x3f326000}
       {x44d24000 x44a64000 x3f35a000}
       {x44d34000 x44b3c000 x3f3d2000}
       {x44d30000 x44ba8000 x3f3d2000}
       {x44d2c000 x44b6c000 x3f3da000}
       {x44d50000 x44a74000 x3f426000}
       {x44d58000 x449d4000 x3f432000}
       {x44d50000 x44994000}}}
     {t x44d39c72 x44a8b8e4}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x439c8000 bu 1 src 1 stx x41400000 sty x43940000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}
    {cubiccurve Clone14 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44e38000 x44c98000 x3ef00000}
       {x44e58000 x44ccc000 x3f1f6000}
       {x44e60000 x44cd0000 x3f26a000}
       {x44ee4000 x44cc8000 x3f38a000}
       {x44f2c000 x44ca0000 x3f3d2000}
       {x44f34000 x44c90000 x3f3ea000}
       {x44ef0000 x44cd4000 x3f456000}
       {x44e8c000 x44d14000 x3f482000}
       {x44e7c000 x44d18000 x3f29a000}
       {x44e7c000 x44d10000}}}
     {t x44eaa666 x44cd2ccd}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x439c8000 bu 1 src 1 stx x41600000 sty x43a20000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}
    {cubiccurve Clone13 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44ed8000 x44a94000 x3d580000}
       {x44edc000 x44a94000 x3efe0000}
       {x44f5c000 x44a90000 x3f2b2000}
       {x44ff4000 x44a90000 x3f2ee000}
       {x45010000 x44a8c000 x3f2ca000}
       {x45012000 x44a84000 x3f2c2000}
       {x4500a000 x44a88000 x3f2d6000}
       {x4500c000 x44a6c000 x3f31e000}
       {x44ff4000 x44a70000 x3f342000}
       {x44f90000 x44a94000 x3f342000}
       {x44ef4000 x44a98000 x3f2ca000}
       {x44ed0000 x44a94000}}}
     {t x44c55111 x44f1aaab}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x43450000 bu 1 src 1 stx x42680000 sty x42b00000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}
    {cubiccurve Clone2 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44c80000 x44ed6000 x3ea80000}
       {x44c7c000 x44ed6000 x3efa8000}
       {x44c76000 x44eda000 x3f20e000}
       {x44c64000 x44ee4000 x3f34a000}
       {x44c52000 x44eec000 x3f37e000}
       {x44c22000 x44efe000 x3f3ae000}
       {x44c0a000 x44f08000 x3f3c6000}
       {x44bd4000 x44f1a000 x3f3d2000}
       {x44b9e000 x44f30000 x3f3de000}
       {x44b6e000 x44f42000 x3f416000}
       {x44b3c000 x44f58000 x3f426000}
       {x44b26000 x44f62000 x3f42a000}
       {x44af8000 x44f7c000 x3f436000}
       {x44ae6000 x44f8a000 x3f436000}
       {x44ad0000 x44f98000 x3f43a000}
       {x44abe000 x44fa6000 x3f43e000}
       {x44a9e000 x44fbc000 x3f442000}
       {x44a90000 x44fc8000 x3f446000}
       {x44a76000 x44fda000 x3f44a000}
       {x44a68000 x44fe4000 x3f44a000}
       {x44a5e000 x44fee000 x3f44a000}
       {x44a4e000 x44ff6000 x3f44a000}
       {x44a3c000 x45004000 x3f44a000}
       {x44a2e000 x45008000 x3f44e000}
       {x44a2a000 x45009000 x3f452000}
       {x44a28000 x4500b000 x3f456000}
       {x44a28000 x4500d000 x3f456000}
       {x44a24000 x4500d000 x3f456000}
       {x44a24000 x45011000 x3f452000}
       {x44a24000 x45012000 x3f452000}
       {x44a1c000 x45016000 x3f456000}
       {x44a56000 x45008000 x3f4aa000}
       {x44a72000 x44ffe000 x3f4b2000}
       {x44ab0000 x44fd6000 x3f53a000}
       {x44ad0000 x44fc0000 x3f552000}
       {x44bbe000 x44f38000 x3f576000}
       {x44c02000 x44f16000 x3f596000}
       {x44c34000 x44f02000 x3f59a000}
       {x44c4a000 x44efa000 x3f59a000}
       {x44c58000 x44ef2000 x3f58e000}
       {x44c68000 x44eec000}}}
     {t x44b21da9 x44f87c19}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x43450000 bu 1 src 1 stx x42680000 sty x42b00000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}
    {cubiccurve Clone1 512 catmullrom
     {cc
      {f 2080}
      {p
       {x44c40000 x44ede000 x3de20000}
       {x44c3c000 x44ede000 x3f0ae000}
       {x44c40000 x44ede000 x3f1ce000}
       {x44c64000 x44ed6000 x3f362000}
       {x44c6a000 x44ed2000 x3f376000}
       {x44c76000 x44ecc000 x3f396000}
       {x44c80000 x44ec0000 x3f3ae000}
       {x44c8c000 x44eba000 x3f3c6000}
       {x44c96000 x44eae000 x3f3d2000}
       {x44ca0000 x44ea8000 x3f3d6000}
       {x44cac000 x44ea0000 x3f3de000}
       {x44cb6000 x44e98000 x3f3de000}
       {x44cc2000 x44e92000 x3f3e6000}
       {x44cc8000 x44e8e000 x3f3e6000}
       {x44cd0000 x44e8a000 x3f3e6000}
       {x44cd6000 x44e86000 x3f3e6000}
       {x44ce2000 x44e84000 x3f3ea000}
       {x44cec000 x44e7c000 x3f3e6000}
       {x44cf0000 x44e7c000 x3f3e6000}
       {x44cf4000 x44e78000 x3f3e2000}
       {x44ce8000 x44e7c000 x3f3de000}
       {x44cc8000 x44e92000 x3f456000}
       {x44c6e000 x44ecc000 x3f49a000}
       {x44c58000 x44ed6000 x3f492000}
       {x44c40000 x44ee0000 x3f492000}
       {x44b38000 x44f70000 x3f4ee000}
       {x44aea000 x44faa000 x3f50a000}
       {x44abe000 x44fc0000 x3f492000}
       {x44ab0000 x44fc4000 x3f40e000}
       {x44aa8000 x44fc8000 x3f02e000}
       {x44aa8000 x44fc4000}}}
     {t x44c42f7c x44ede94a}
     {a ro 0 go 0 bo 0 ao 0 opc x3dcccccd bs x43450000 bu 1 src 1 stx x42680000 sty x42b00000 str 1 spx x44f00000 spy x44870000 sb 1 ltn x44844000 ltm x44844000 ltt x40000000 tt x41980000}}}}}}
toolbox {clone {
  { selectAll opc 0.1 bs 313 src 1 str 1 ssx 1 ssy 1 sf 1 }
  { createBezier str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createBezierCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createBSpline str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createEllipse str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangle str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangleCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { brush str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { eraser src 2 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { clone opc 0.1 bs 313 src 1 stx 24 sty 212 str 1 ssx 1 ssy 1 sf 1 sb 1 ltn 1058 ltm 1058 tt 19 }
  { reveal src 3 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { dodge src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { burn src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { blur src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { sharpen src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { smear src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
} }
brush_hardness 0.200000003
source_black_outside true
name RotoPaint2
xpos -14008
ypos -6943
}
"""

    result_dict = SceneParser(input_string)
    pprint(result_dict.get_dict())
    pprint(result_dict.groups())
    # pprint(result_dict.groups(False))
