# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = link = ViewPageTemplateFile('templates/plugin.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._setup()

    def _setup(self):
        portal = api.portal.get()
        self.sendto_form = portal.absolute_url() + '/sendto_form'
