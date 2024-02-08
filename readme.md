This api is for creating nuke scene without using nuke.
By using same command as nuke api it'll generated a nuke scene .nk.

This api also generate un dictionary for each node inside a scene.

# API
```python
nuke = NukeCmds()
read = nuke.createNode("Read")
check = nuke.createNode("CheckerBoard")
grade = nuke.createNode("Grade")
noop = nuke.createNode("NoOp")
noop2 = nuke.createNode("NoOp")

read.knob("file").setValue("kdkdkdkdkdkd")
grade.setInput(0, noop)
grade.setXYPos(noop.xpos(), noop.ypos() + 50)
noop2.setXYPos(250, 53)

nuke.scriptSaveAs('test_file_out')
```

### path.nk
```
Root {
 name 
 inputs 0
 xpos 0
 ypos 0
 format 2048 1556 0 0 2048 1556 1 2K_Super_35(full-ap)
 proxy_format 1024 778 0 0 1024 778 1 1K_Super_35(full-ap)
 colorManagement Nuke
 workingSpaceLUT linear
 monitorLut sRGB
 monitorOutLUT rec709
 int8Lut sRGB
 int16Lut sRGB
 logLut Cineon
 floatLut linear
}
Read {
 name Read1
 inputs 0
 xpos 0
 ypos 50
 file kdkdkdkdkdkd
}
CheckerBoard {
 name CheckerBoard1
 inputs 0
 xpos 0
 ypos 150
}
NoOp {
 name NoOp1
 inputs 0
 xpos 0
 ypos 750
}
Grade {
 name Grade1
 xpos 0
 ypos 800
}
NoOp {
 name NoOp2
 inputs 0
 xpos 250
 ypos 53
}
```
