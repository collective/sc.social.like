# -*- coding:utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile
from sc.social.like.logger import logger


def apply_profile(context):
    """ Apply upgrade profile """
    profile = 'profile-sc.social.like.upgrades.v2000:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 2000')
