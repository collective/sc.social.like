# -*- coding:utf-8 -*-
from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    enabled_portal_types = []
    typebutton = ''
    twitter_enabled = ''
    twittvia = ''
    language = 'en'

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = get_language(context)
        self.urlnoscript = (
            u'http://twitter.com/home?status=' +
            url_quote(u'{0} - {1} via {2}'.format(
                safe_unicode(self.context.title),
                self.context.absolute_url(),
                self.twittvia)
            )
        )

    @property
    def typebutton(self):
        return api.portal.get_registry_record('sc.social.like.typebutton')

    @property
    def twittvia(self):
        return api.portal.get_registry_record('sc.social.like.twittvia')

    def share_link(self):
        params = dict(
            text=self.context.Title(),
            url=self.context.absolute_url(),
        )
        if self.twittvia:
            params['via'] = self.twittvia

        url = 'https://twitter.com/intent/tweet?' + urlencode(params)
        return url
