# -*- coding:utf-8 -*-
from sc.social.like.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    ''' Apply upgrade profile '''
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-sc.social.like.upgrades.v2000:default'
    loadMigrationProfile(context, profile)
    logger.info('Applied upgrade profile to version 2000')
