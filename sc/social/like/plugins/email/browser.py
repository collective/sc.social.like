# -*- coding:utf-8 -*-
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    metadata = None
    plugin = link = ViewPageTemplateFile('plugin.pt')
