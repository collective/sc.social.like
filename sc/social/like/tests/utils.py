# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from sc.social.like.behaviors import ISocialMedia
from zope.component import getUtility
from zope.event import notify


def enable_social_media_behavior():
    fti = getUtility(IDexterityFTI, name='News Item')
    behaviors = list(fti.behaviors)
    behaviors.append(ISocialMedia.__identifier__)
    fti.behaviors = tuple(behaviors)
    # invalidate schema cache
    notify(SchemaInvalidatedEvent('News Item'))


def get_random_string(length):
    from random import choice
    from string import printable
    return ''.join(choice(printable) for i in xrange(0, length))
