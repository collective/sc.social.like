# -*- coding:utf-8 -*-
from zope.interface import Interface


class IPlugin(Interface):
    ''' A Social Like Plugin '''

    def config_view():
        ''' Plugin configuration '''

    def view():
        ''' Plugin's browser view '''

    def metadata():
        ''' Return metadata method '''

    def plugin():
        ''' Return html render method '''


class IPluginView(Interface):
    ''' A Social Like Plugin Browser View '''

    def metadata():
        ''' Return metadata method '''

    def plugin():
        ''' Return html render method '''
