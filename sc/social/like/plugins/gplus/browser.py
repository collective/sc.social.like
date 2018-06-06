# -*- coding:utf-8 -*-
"""Helper view to generate Google+ widget.

More information:
* https://developers.google.com/+/web/share/
"""
from six.moves.urllib.parse import urlencode  # noqa: I001
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language


class PluginView(BrowserView):
    """Helper view to generate Google+ widget."""

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
        return get_language(self.context)

    def annotation(self):
        """Return annotation to display next to the button."""
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        typebutton = api.portal.get_registry_record(record, default='')

        if typebutton == 'vertical':
            return 'vertical-bubble'
        return 'bubble'

    def share_link(self):
        # Does we need any special language handler?
        # See https://developers.google.com/+/web/share/?hl=it#available-languages
        params = dict(
            url=self.context.absolute_url(),
            hl=self.language,
        )
        url = 'https://plus.google.com/share?' + urlencode(params)
        return url
