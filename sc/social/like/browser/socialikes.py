# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
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
        try:
            enabled_portal_types = api.portal.get_registry_record(record)
        except InvalidParameterError:
            enabled_portal_types = []

        return self.context.portal_type in enabled_portal_types
