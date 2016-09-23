# -*- coding:utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName
from sc.social.like.logger import logger


def cook_css_registry(context):
    """ Apply upgrade profile """
    css_registry = getToolByName(context, 'portal_css')
    css_registry.cookResources()
    logger.info('CSS registry refreshed')


def apply_profile(context):
    """ Apply upgrade profile """
    profile = 'profile-sc.social.like.upgrades.v3010:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3010')


def remove_actionicons(context):
    """ Remove registration from deprecated actionicons tool"""
    portal_actionicons = getToolByName(context, 'portal_actionicons')
    try:
        portal_actionicons.removeActionIcon('controlpanel', 'sociallikes')
        logger.info('Removed deprecated registration on portal_actionicons tool')
    except KeyError:
        pass
