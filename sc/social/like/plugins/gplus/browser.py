# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    typebutton = ''
    gp_enabled = True
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

    @property
    def typebutton(self):
        typebutton = api.portal.get_registry_record('sc.social.like.typebutton')
        if typebutton == 'horizontal':
            typebutton = 'medium'
        else:
            typebutton = 'tall'
        return typebutton

    def share_link(self):
        # Does we need any special language handler?
        # See https://developers.google.com/+/web/share/?hl=it#available-languages
        params = dict(
            url=self.context.absolute_url(),
            hl=self.language,
        )
        url = 'https://plus.google.com/share?' + urlencode(params)
        return url
