# -*- coding:utf-8 -*-

import logging
from Products.CMFCore.utils import getToolByName
from sc.social.like.config import PROJECTNAME


def cook_css_registry(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    css_registry = getToolByName(context, 'portal_css')
    css_registry.cookResources()
    logger.info('CSS registry refreshed')
