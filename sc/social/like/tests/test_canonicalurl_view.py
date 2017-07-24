# -*- coding: utf-8 -*-
"""Test for the canonical URL updater form."""
from DateTime import DateTime
from plone import api
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import HAS_DEXTERITY
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.tests.utils import enable_social_media_behavior

import unittest


if not HAS_DEXTERITY:
    # skip all tests if not running on Dexterity-based content types
    def test_suite():
        return unittest.TestSuite()


class CanonicalURLUpdaterTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        enable_social_media_behavior()
        self.setup_content()
        api.portal.set_registry_record(
            name='canonical_domain', value='https://example.org', interface=ISocialLikeSettings)

    def setup_content(self):
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(self.portal, type='News Item', id='foo')
            api.content.transition(obj, 'publish')
            obj = api.content.create(self.portal, type='News Item', id='bar')
            api.content.transition(obj, 'publish')
            obj = api.content.create(self.portal, type='News Item', id='baz')
            api.content.transition(obj, 'publish')

        # simulate objects were create way long in the past
        self.portal['foo'].effective_date = DateTime('2015/01/01')
        self.portal['foo'].reindexObject()
        self.portal['bar'].effective_date = DateTime('2016/01/01')
        self.portal['bar'].reindexObject()
        # XXX: publishing an object does not sets its effective date
        #      https://github.com/plone/plone.api/issues/343
        self.portal['baz'].effective_date = DateTime()
        self.portal['baz'].reindexObject()

    @unittest.expectedFailure  # FIXME: https://github.com/collective/sc.social.like/issues/119
    def test_update_canonical_url(self):
        # canonical URL is None as we did not set up a canonical domain
        self.assertIsNone(self.portal['foo'].canonical_url)
        self.assertIsNone(self.portal['bar'].canonical_url)
        self.assertIsNone(self.portal['baz'].canonical_url)

        name = 'canonical-url-updater'
        view = api.content.get_view(name, self.portal, self.request)
        # simulate data comming from form
        data = dict(
            old_canonical_domain='http://example.org',
            published_before=DateTime('2017/01/01').asdatetime(),
        )
        view.update_canonical_url(data)
        # objects created before the specified date will have their
        # canonical URL updated
        self.assertEqual(
            self.portal['foo'].canonical_url, 'http://example.org/plone/foo')
        self.assertEqual(
            self.portal['bar'].canonical_url, 'http://example.org/plone/bar')
        # objects created after the specified date will have their
        # canonical URL unchaged
        self.assertEqual(
            self.portal['baz'].canonical_url, 'https://example.org/plone/baz')
