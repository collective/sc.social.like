# -*- coding:utf-8 -*-
"""Helper view to generate Email widget."""
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings


class PluginView(BrowserView):
    """Helper view to generate Email widget."""

    metadata = None
    plugin = link = ViewPageTemplateFile('plugin.pt')

    @property
    def klass(self):
        klass = 'share-by-email pat-plone-modal'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        do_not_track = api.portal.get_registry_record(record, default=False)
        if do_not_track:
            klass += ' link'
        return klass
