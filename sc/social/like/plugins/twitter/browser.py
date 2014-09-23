# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    enabled_portal_types = []
    typebutton = ''
    twitter_enabled = ''
    twittvia = ''
    language = 'en'

    metadata = ViewPageTemplateFile("templates/metadata.pt")
    plugin = ViewPageTemplateFile("templates/plugin.pt")

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = get_language(context)
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        if self.sheet:
            self.typebutton = self.sheet.getProperty("typebutton", "")
            self.twittvia = self.sheet.getProperty("twittvia", "")
        self.urlnoscript = (
            u'http://twitter.com/home?status=' +
            url_quote(u'{0} - {1} via {2}'.format(
                safe_unicode(self.context.title),
                self.context.absolute_url(),
                self.twittvia)
            )
        )
