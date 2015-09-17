# -*- coding: utf-8 -*-
from sc.social.like.config import PROJECTNAME
from plone import api


def remove_properties(portal):
    portal_properties = api.portal.get_tool(name='portal_properties')
    try:
        portal_properties.manage_delObjects(ids='sc_social_likes_properties')
    except KeyError:
        pass


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_properties(portal)
        profile = 'profile-%s:uninstall' % PROJECTNAME
        setup_tool = api.portal.get_tool(name='portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
