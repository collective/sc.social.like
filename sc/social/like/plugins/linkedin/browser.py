# -*- coding:utf-8 -*-
"""Helper view to generate LinkedIn widget.

More information:
* https://developer.linkedin.com/plugins/share
* https://developer.linkedin.com/docs/share-on-linkedin
"""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language
from urllib import urlencode


class PluginView(BrowserView):
    """Helper view to generate LinkedIn widget."""

    metadata = None
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

    def portal_url(self):
        portal = api.portal.get()
        return portal.absolute_url()

    def language(self):
        # XXX: future use
        return get_language(self.context)

    def counter(self):
        """Return plugin count mode."""
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        typebutton = api.portal.get_registry_record(record, default='')

        if typebutton == 'vertical':
            return 'top'
        return 'right'

    def share_link(self):
        params = {
            'mini': 'true',
            'url': self.context.absolute_url(),
            'title': self.context.Title(),
            'summary': self.context.Description(),
        }
        url = 'https://www.linkedin.com/shareArticle?' + urlencode(params)
        return url
