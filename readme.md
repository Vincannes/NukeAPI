This api is for creating nuke scene without using nuke.
By using same command as nuke api it'll generated a nuke scene .nk.

# API
```python
nuke = NukeCmds()
check = nuke.createNode("CheckerBoard")
grade = nuke.createNode("Grade")
noop = nuke.createNode("NoOp")
grade.setInput(0, noop)
grade.setXYPos(noop.xpos(), noop.ypos() + 50)
nuke.scriptSaveAs("path.nk")
```

```path.nk
CheckerBoard {
 name CheckerBoard1
 inputs 0
 xpos 0
 ypos 0
}
NoOp {
 name NoOp1
 inputs 0
 xpos 0
 ypos 150
}
Grade {
 name Grade1
 xpos 0
 ypos 200
}
```
