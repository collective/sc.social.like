# -*- coding:utf-8 -*-
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from plone.api.exc import InvalidParameterError
from plone import api
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter


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
        self.portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = self.context.absolute_url()
        self.language = get_language(self.context)
        data = url_quote(self.context.absolute_url())
        self.telegramurl = u'https://telegram.me/share/url?url={0}'.format(data)

    @property
    def klass(self):
        klass = 'telegram'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        try:
            do_not_track = api.portal.get_registry_record(record)
        except InvalidParameterError:
            do_not_track = False
        if do_not_track:
            klass += ' link'
        return klass
