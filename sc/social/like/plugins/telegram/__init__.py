# -*- coding:utf-8 -*-
"""Utility and helper view to generate Telegram widget."""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implementer


class PluginView(BrowserView):
    """Helper view to generate Telegram widget."""

    metadata = None
    plugin = link = ViewPageTemplateFile('plugin.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self._setup()

    def _setup(self):
        self.url = self.context.absolute_url()
        data = url_quote(self.context.absolute_url())
        self.telegramurl = u'https://telegram.me/share/url?url={0}'.format(data)

    @property
    def klass(self):
        klass = 'telegram'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        do_not_track = api.portal.get_registry_record(record, default=False)
        if do_not_track:
            klass += ' link'
        return klass


@implementer(IPlugin)
class Telegram(Plugin):

    id = 'telegram'
    name = 'Telegram'

    def config_view(self):
        # No configuration view
        return None
