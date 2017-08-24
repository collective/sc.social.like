# -*- coding:utf-8 -*-
from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    twitter_enabled = False
    language = 'en'

    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        self.title = self.context.title
        self.description = self.context.Description()
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()
        self.portal_title = portal_state.portal_title()
        self.url = self.context.absolute_url()
        self.language = get_language(self.context)
        self.urlnoscript = (
            u'http://twitter.com/home?status=' +
            url_quote(u'{0} - {1} via {2}'.format(
                safe_unicode(self.context.title),
                self.context.absolute_url(),
                self.via)
            )
        )

    @property
    def typebutton(self):
        record = dict(
            name='typebutton', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    @property
    def via(self):
        record = dict(
            name='twitter_username', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    def share_link(self):
        params = dict(
            text=safe_unicode(self.context.Title()).encode('utf-8'),
            url=self.context.absolute_url(),
        )
        if self.via:
            params['via'] = self.via
        return 'https://twitter.com/intent/tweet?' + urlencode(params)
