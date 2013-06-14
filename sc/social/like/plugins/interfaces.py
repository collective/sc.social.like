# -*- coding:utf-8 -*-
from zope.interface import Interface


class IPlugin(Interface):
    ''' A Social Like Plugin '''

    id = ''
    name = ''

    def config_view():
        pass

    def view(self):
        pass

    def metadata(self):
        pass

    def plugin(self):
        pass


class IPluginView(Interface):
    ''' A Social Like Plugin Browser View '''

    def metadata():
        pass

    def plugin():
        pass
