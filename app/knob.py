#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

class Knob(object):

    def __init__(self, name, defaut_val="", parent=None):
        self.name = name
        self._value = defaut_val
        self._parent = parent

    def __repr__(self):
        return "{} | {}".format(self.__class__, self.name)

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value
        self._parent._knobs_dict[self.name] = value

    def setExpression(self, expression=""):
        NotImplementedError
