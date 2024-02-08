#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import json

from pprint import pprint
from io_file import SceneParser

path_json = "D:\\Desk\\python\\NukeAPI\\tests\\test.json"
test_file = "D:\\Desk\\python\\NukeAPI\\tests\\test.nk"
test_file_out = "D:\\Desk\\python\\NukeAPI\\tests\\test_final.nk"
_aaa = "D:\\Desk\\python\\NukeAPI\\tests\\083_060-cmp-base-v016.nk"

with open(_aaa, 'r') as file:
    file_content = file.read()

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

# scene_parser = SceneParser(file_content)
# json_object = json.dumps(scene_parser.get_dict(), indent=4)

# with open(path_json, "w") as outfile:
#     outfile.write(json_object)

with open(path_json, "r") as _file:
    load_scene = json.load(_file)

scene = SceneParser(input_string)
# scene.update_dict(load_scene)

# pprint(scene.get_dict())
scene.dict_to_scene(test_file)
# pprint(load_scene.get("Tracker4"))
