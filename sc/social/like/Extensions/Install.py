# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.config import PROJECTNAME


def remove_tiles():
    from sc.social.like.config import TILES
    registered = api.portal.get_registry_record('plone.app.tiles')
    [registered.remove(t) for t in TILES if t in registered]


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_tiles()
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool(name='portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
