# -*- coding:utf-8 -*-
"""Helper view to generate Twitter widget.

More information:
* https://dev.twitter.com/web/tweet-button
* https://dev.twitter.com/web/overview/privacy
"""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from urllib import urlencode


class PluginView(BrowserView):
    """Helper view to generate Twitter widget."""

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

    @property
    def is_plone_5(self):
        return IS_PLONE_5

    def portal_url(self):
        portal = api.portal.get()
        return portal.absolute_url()

    def canonical_url(self):
        """Return canonical URL if available; otherwise, context URL."""
        if ISocialMedia.providedBy(self.context):
            return self.context.canonical_url
        else:
            return self.context.absolute_url()

    def via(self):
        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        return api.portal.get_registry_record(record, default='')

    def share_link(self):
        params = {
            'text': self.context.Title(),
            'url': self.context.absolute_url(),
        }

        via = self.via()
        if via:
            params['via'] = via

        url = 'https://twitter.com/intent/tweet?' + urlencode(params)
        return url

    def dnt(self):
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        return api.portal.get_registry_record(record, default=False)
