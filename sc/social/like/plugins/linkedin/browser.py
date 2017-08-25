# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
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
        # FIXME: the following could rise unexpected exceptions
        #        move it to a new setup() method
        #        see: http://docs.plone.org/develop/plone/views/browserviews.html#creating-a-view
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.url = context.absolute_url()

    @property
    def typebutton(self):
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        try:
            typebutton = api.portal.get_registry_record(record)
        except InvalidParameterError:
            typebutton = ''

        if typebutton == 'horizontal':
            typebutton = 'right'
        else:
            typebutton = 'top'
        return typebutton

    def share_link(self):
        params = dict(
            mini='true',
            url=self.context.absolute_url(),
            title=self.context.Title(),
            summary=self.context.Description(),
        )
        url = 'https://www.linkedin.com/shareArticle?' + urlencode(params)
        return url
