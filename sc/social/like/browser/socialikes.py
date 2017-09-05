# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from sc.social.like.interfaces import ISocialLikes
from sc.social.like.interfaces import ISocialLikeSettings
from zope.interface import implementer


@implementer(ISocialLikes)
class SocialLikes(BrowserView):
    """
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled in this context."""
        record = ISocialLikeSettings.__identifier__ + '.enabled_portal_types'
        enabled_portal_types = api.portal.get_registry_record(record, default=[])
        return self.context.portal_type in enabled_portal_types
