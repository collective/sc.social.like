# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from urllib import urlencode
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    linkedin_enabled = True

    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()
        self.url = self.context.absolute_url()

    @property
    def typebutton(self):
        record = dict(
            name='typebutton', interface=ISocialLikeSettings, default='')
        if api.portal.get_registry_record(**record) == 'horizontal':
            return 'right'
        return 'top'

    def share_link(self):
        params = dict(
            mini='true',
            url=self.context.absolute_url(),
            title=self.context.Title(),
            summary=self.context.Description(),
        )
        return 'https://www.linkedin.com/shareArticle?' + urlencode(params)
