# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from sc.social.like.interfaces import ISocialLikes

_ = MessageFactory('sc.social.like')


class SocialLikes(BrowserView):
    """
    """
    implements(ISocialLikes)

    enabled_portal_types = []

    def __init__(self, context, request, *args, **kwargs):
        super(SocialLikes, self).__init__(context, request, *args, **kwargs)
        context = aq_inner(context)
        self.context = context
        pp = getToolByName(context, 'portal_properties')
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        if self.sheet:
            self.enabled_portal_types = self.sheet.getProperty(
                "enabled_portal_types"
            )

    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled
           for this context"""
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types
