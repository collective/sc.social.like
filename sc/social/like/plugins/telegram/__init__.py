# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter
from zope.interface import implementer


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    plugin = link = ViewPageTemplateFile('plugin.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()
        self.portal_title = portal_state.portal_title()
        self.url = self.context.absolute_url()
        self.language = get_language(self.context)
        data = url_quote(self.context.absolute_url())
        self.telegramurl = u'https://telegram.me/share/url?url={0}'.format(data)

    @property
    def klass(self):
        klass = 'telegram'
        record = dict(
            name='do_not_track', interface=ISocialLikeSettings, default=False)
        if api.portal.get_registry_record(**record):
            return klass + ' link'
        return klass


@implementer(IPlugin)
class Telegram(Plugin):

    id = 'telegram'
    name = 'Telegram'

    def config_view(self):
        # No configuration view
        return None
