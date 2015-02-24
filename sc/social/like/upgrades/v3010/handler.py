# -*- coding:utf-8 -*-

import logging
from Products.CMFCore.utils import getToolByName
from sc.social.like.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile


def cook_css_registry(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    css_registry = getToolByName(context, 'portal_css')
    css_registry.cookResources()
    logger.info('CSS registry refreshed')

def apply_profile(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-sc.social.like.upgrades.v3010:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3010')
