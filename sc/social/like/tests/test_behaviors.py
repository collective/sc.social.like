# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from plone.registry.interfaces import IRegistry
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import DEXTERITY
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtility
from zope.event import notify

import unittest


if not DEXTERITY:
    # skip all tests if not running on Dexterity-based content types
    def test_suite():
        return unittest.TestSuite()


class BehaviorsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _enable_social_media_behavior(self):
        fti = getUtility(IDexterityFTI, name='News Item')
        behaviors = list(fti.behaviors)
        behaviors.append(ISocialMedia.__identifier__)
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent('News Item'))

    def setUp(self):
        self.portal = self.layer['portal']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISocialLikeSettings)
        self.settings.canonical_domain = 'http://example.org'
        self._enable_social_media_behavior()

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(self.portal, 'News Item', 'foo')

    def test_socialmedia_behavior(self):
        self.assertTrue(ISocialMedia.providedBy(self.obj))

    def test_canonical_url(self):
        self.assertEqual(self.obj.canonical_url, 'http://example.org/plone/foo')
