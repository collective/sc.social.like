# -*- coding: utf-8 -*-
from six.moves import range  # noqa: I001
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
    return ''.join(choice(printable) for i in range(0, length))


def get_file(filename):
    """Return contents of file from current directory."""
    import os
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'images', filename)
    with open(path, 'rb') as f:
        return f.read()


def get_file_b64encoded(filename):
    """Load file from current directory and return it b64encoded."""
    from plone.formwidget.namedfile.converter import b64encode_file
    data = get_file(filename)
    return b64encode_file(filename, data)
