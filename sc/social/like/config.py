# -*- coding: utf-8 -*-
from plone import api


PROJECTNAME = 'sc.social.like'

DEFAULT_ENABLED_CONTENT_TYPES = ('Document', 'Event', 'News Item')
DEFAULT_PLUGINS_ENABLED = ('Facebook', 'Twitter')

TILES = [
    u'sc.social.like.facebook',
    u'sc.social.like.twitter',
]

IS_PLONE_5 = api.env.plone_version().startswith('5')
