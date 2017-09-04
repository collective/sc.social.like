# -*- coding:utf-8 -*-
"""Helper view to generate Pinterest widget.

More information:
* https://developers.pinterest.com/docs/widgets/save/
* https://developers.pinterest.com/docs/rich-pins/reference/
"""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_content_image
from urllib import urlencode


class PluginView(BrowserView):
    """Helper view to generate Pinterest widget."""

    metadata = None
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

    def portal_url(self):
        portal = api.portal.get()
        return portal.absolute_url()

    def image_url(self):
        """Return URL to image."""
        image = get_content_image(self.context, scale='large')
        if image:
            return image.url
        else:
            return self.portal_url() + '/logo.png'

    def pin_count(self):
        """Return pin count mode."""
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        typebutton = api.portal.get_registry_record(record, default='')

        if typebutton == 'vertical':
            return 'above'
        return 'beside'

    def share_link(self):
        # See https://stackoverflow.com/a/11212220
        params = {
            'url': self.context.absolute_url(),
            'media': self.image_url(),
            'description': self.context.Title(),
        }
        url = 'https://pinterest.com/pin/create/button/?' + urlencode(params)
        return url
