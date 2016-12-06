# -*- coding: utf-8 -*-
from mock import Mock
from plone import api
from sc.social.like.testing import HAS_COVER
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from sc.social.like.tiles.twitter import ITwitterTile
    from sc.social.like.tiles.twitter import TwitterTile
else:
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


class TwitterTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(TwitterTileTestCase, self).setUp()
        self.tile = TwitterTile(self.cover, self.request)
        self.tile.__name__ = u'sc.social.like.twitter'
        self.tile.id = u'test'

    def _set_record(self, name, value):
        from sc.social.like.interfaces import ISocialLikeSettings
        api.portal.set_registry_record(
            name=name, value=value, interface=ISocialLikeSettings)

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = ITwitterTile
        self.klass = TwitterTile
        super(TwitterTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertFalse(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_is_empty(self):
        self.assertTrue(self.tile.is_empty)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), [])

    def test_username_not_set(self):
        self.assertEqual(self.tile.username, '')

    def test_username_set(self):
        self._set_record('twitter_username', 'plone')
        self.assertEqual(self.tile.username, 'plone')

    def test_get_data(self):
        expected = dict(
            aria_polite=None,
            chrome='',
            height=None,
            tweet_limit=None,
            widget_id=None,
            width=None,
        )
        self.assertEqual(self.tile.get_data, expected)

    def test_render_empty(self):
        msg = u'you must define a Twitter username'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_render_not_empty(self):
        self._set_record('twitter_username', 'plone')
        rendered = self.tile()
        self.assertIn(u'twitter-timeline', rendered)
