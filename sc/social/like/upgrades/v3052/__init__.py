# -*- coding:utf-8 -*-
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from zope.component import queryUtility


def enable_social_media_behavior(context):
    """Enable Social Media behavior."""
    enabled_portal_types = api.portal.get_registry_record(
        name='enabled_portal_types', interface=ISocialLikeSettings)

    types = []
    for t in enabled_portal_types:
        fti = queryUtility(IDexterityFTI, name=t)
        if fti is None:
            continue  # not a Dexterity-based content type

        behaviors = list(fti.behaviors)
        if ISocialMedia.__identifier__ in behaviors:
            continue  # nothing to do

        behaviors.append(ISocialMedia.__identifier__)
        fti.behaviors = tuple(behaviors)
        types.append(t)

    if types:
        types = ', '.join(types)
        msg = 'Social Media behavior was enabled for the following content types: {0}'.format(types)
        logger.info(msg)
