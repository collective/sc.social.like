# -*- coding:utf-8 -*-
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from zope.component import getUtility


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(ISocialLikeSettings)

    logger.info('Done.')
