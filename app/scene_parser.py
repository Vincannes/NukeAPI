#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

from app.io_file import SceneDict


class SceneParser(object):

    def __init__(self, path=None):
        dict_scene = SceneDict(path)
