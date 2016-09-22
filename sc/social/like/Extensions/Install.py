# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.config import PROJECTNAME
from sc.social.like.config import TILES


def remove_tile(tile):
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if tile in tiles:
        tiles.remove(tile)


def uninstall(portal, reinstall=False):
    if not reinstall:
        map(remove_tile, TILES)
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool(name='portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
