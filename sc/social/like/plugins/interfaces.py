# -*- coding:utf-8 -*-
from zope.interface import Interface


class IPlugin(Interface):
    pass


class IPluginView(Interface):
    def metadata():
        pass

    def plugin():
        pass
