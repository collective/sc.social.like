# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.twitter import controlpanel
from sc.social.like.utils import facebook_language
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    enabled_portal_types = []
    typebutton = ''
    twitter_enabled = ''
    twittvia = ''
    language = 'en_US'

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
        languages = self.request.get('HTTP_ACCEPT_LANGUAGE',
                                     '').split(';')[0].split(',')
        self.language = facebook_language(languages, self.language)
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        if self.sheet:
            self.typebutton = self.sheet.getProperty("typebutton", "")
            self.twittvia = self.sheet.getProperty("twittvia", "")

    @property
    def prefs(self):
        portal = self.portal
        return controlpanel.ITwitterSchema(portal)
