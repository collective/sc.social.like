# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
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

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # FIXME: the following could rise unexpected exceptions
        #        move it to a new setup() method
        #        see: http://docs.plone.org/develop/plone/views/browserviews.html#creating-a-view
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
                self.via)
            )
        )

    @property
    def typebutton(self):
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        try:
            return api.portal.get_registry_record(record)
        except InvalidParameterError:
            return ''

    @property
    def via(self):
        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        try:
            return api.portal.get_registry_record(record)
        except InvalidParameterError:
            return ''

    def share_link(self):
        params = dict(
            text=self.context.Title(),
            url=self.context.absolute_url(),
        )
        if self.via:
            params['via'] = self.via

        url = 'https://twitter.com/intent/tweet?' + urlencode(params)
        return url
