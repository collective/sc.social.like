# -*- coding:utf-8 -*-
from plone import api
from sc.social.like.config import TILES
from sc.social.like.logger import logger


def register_cover_tiles(setup_tool):
    """Register collective.cover tiles."""
    registered = api.portal.get_registry_record('plone.app.tiles')
    [registered.append(t) for t in TILES if t not in registered]
    assert set(registered) & set(TILES) == set(TILES)
    logger.info('Tiles for collective.cover were registered')
