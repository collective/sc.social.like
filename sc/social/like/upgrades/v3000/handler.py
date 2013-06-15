# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sc.social.like.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-sc.social.like.upgrades.v3000:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3000')


def update_plugins(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    pp = getToolByName(context, 'portal_properties')
    sheet = getattr(pp, 'sc_social_likes_properties', None)
    plugins_enabled = []
    if sheet.twitter_enabled:
        plugins_enabled.append('Twitter')
    if sheet.fb_enabled:
        plugins_enabled.append('Facebook')
    if sheet.gp_enabled:
        plugins_enabled.append('Google+')
    sheet.manage_changeProperties(plugins_enabled=plugins_enabled)
    logger.info('Update enabled plugins list')
