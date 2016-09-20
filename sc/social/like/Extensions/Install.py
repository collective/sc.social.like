# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.config import PROJECTNAME


def uninstall(portal, reinstall=False):
    if not reinstall:
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool(name='portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
