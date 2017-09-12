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

# social networks sharing best practices
OG_TITLE_MAX_LENGTH = 70
OG_DESCRIPTION_MAX_LENGTH = 200
OG_LEAD_IMAGE_MIME_TYPES = ('image/jpeg', 'image/png', 'image/gif', ' image/webp')
OG_LEAD_IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5MB
OG_LEAD_IMAGE_MIN_HEIGHT = 315
OG_LEAD_IMAGE_MIN_WIDTH = 600
OG_LEAD_IMAGE_MIN_ASPECT_RATIO = 1.33
