# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from sc.social.like.interfaces import ISocialLikes
from zope.interface import implements


class SocialLikes(BrowserView):
    """
    """
    implements(ISocialLikes)

    enabled_portal_types = []

    def __init__(self, context, request, *args, **kwargs):
        super(SocialLikes, self).__init__(context, request, *args, **kwargs)
        context = aq_inner(context)
        self.context = context

    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled
           for this context"""
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types

    @property
    def enabled_portal_types(self):
        return api.portal.get_registry_record('sc.social.like.enabled_portal_types')
