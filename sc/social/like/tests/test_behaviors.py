# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import HAS_DEXTERITY
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.tests.utils import enable_social_media_behavior
from zope.component import getUtility

import unittest


if not HAS_DEXTERITY:
    # skip all tests if not running on Dexterity-based content types
    def test_suite():
        return unittest.TestSuite()


class BehaviorsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISocialLikeSettings)
        self.settings.canonical_domain = 'http://example.org'
        enable_social_media_behavior()

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(self.portal, 'News Item', 'foo')

    def test_socialmedia_behavior(self):
        self.assertTrue(ISocialMedia.providedBy(self.obj))

    @unittest.expectedFailure  # FIXME: https://github.com/collective/sc.social.like/issues/119
    def test_canonical_url(self):
        # canonical URL is empty after creation
        self.assertIsNone(self.obj.canonical_url)
        # canonical URL is filled after publishing
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')
        self.assertEqual(self.obj.canonical_url, 'http://example.org/plone/foo')

    def test_canonical_url_with_package_uninstalled(self):
        from sc.social.like.config import PROJECTNAME
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        # don't fail if packege uninstalled
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')
        self.assertIsNone(self.obj.canonical_url)
