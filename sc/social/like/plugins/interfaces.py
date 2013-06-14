# -*- coding:utf-8 -*-
from zope.interface import Interface


class IPlugin(Interface):
    ''' A Social Like Plugin '''

    def config_view():
        pass

    def view():
        pass

    def metadata():
        pass

    def plugin():
        pass


class IPluginView(Interface):
    ''' A Social Like Plugin Browser View '''

    def metadata():
        pass

    def plugin():
        pass
