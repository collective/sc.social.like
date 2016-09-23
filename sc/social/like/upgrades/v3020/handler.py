# -*- coding:utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile
from sc.social.like.logger import logger


def add_privacy_setting(context):
    """ Apply upgrade profile """
    profile = 'profile-sc.social.like.upgrades.v3020:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3020')
