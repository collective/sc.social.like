# -*- coding: utf-8 -*-
from mock import Mock
from plone import api
from sc.social.like.testing import HAS_COVER
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from sc.social.like.tiles.facebook import IFacebookTile
    from sc.social.like.tiles.facebook import FacebookTile
else:
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


class FacebookTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(FacebookTileTestCase, self).setUp()
        self.tile = FacebookTile(self.cover, self.request)
        self.tile.__name__ = u'sc.social.like.facebook'
        self.tile.id = u'test'

    def _set_record(self, name, value):
        from sc.social.like.interfaces import ISocialLikeSettings
        api.portal.set_registry_record(
            name=name, value=value, interface=ISocialLikeSettings)

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IFacebookTile
        self.klass = FacebookTile
        super(FacebookTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertFalse(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_is_empty(self):
        self.assertTrue(self.tile.is_empty)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), [])

    def test_appId_not_set(self):
        self.assertEqual(self.tile.appId, '')

    def test_appId_set(self):
        self._set_record('facebook_app_id', 'dummy')
        self.assertEqual(self.tile.appId, 'dummy')

    def test_get_data(self):
        self._set_record('facebook_app_id', 'dummy')
        self.tile.data['href'] = 'https://www.facebook.com/plone'
        expected = (
            'hide_cover=false&'
            'small_header=false&'
            'tabs=timeline&'
            'height=500&'
            'width=500&'
            'hide_cta=false&'
            'show_facepile=true&'
            'href=https%3A%2F%2Fwww.facebook.com%2Fplone&'
            'adapt_container_width=true&'
            'dummy'
        )
        self.assertEqual(self.tile.get_data, expected)

    def test_render_empty(self):
        msg = u'you must define a Facebook application ID'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_render_not_empty(self):
        self._set_record('facebook_app_id', 'dummy')
        rendered = self.tile()
        self.assertIn(u'<iframe src="//www.facebook.com/plugins', rendered)
