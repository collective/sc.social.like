# -*- coding:utf-8 -*-
import logging
from sc.social.like.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

logger = logging.getLogger(PROJECTNAME)


def add_privacy_setting(context):
    """ Apply upgrade profile """
    profile = 'profile-sc.social.like.upgrades.v3020:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 3020')
