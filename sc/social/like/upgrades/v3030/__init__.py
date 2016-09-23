# -*- coding:utf-8 -*-
from sc.social.like.config import PROJECTNAME
from sc.social.like.logger import logger


def move_mobile_detection_client_side(setup_tool):
    """Fix caching issues with WhatsApp button."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'jsregistry')
    logger.info('Client-side mobile detection now in place.')
