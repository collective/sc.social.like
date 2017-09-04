# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.pinterest import browser
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from zope.component import getUtilitiesFor
from zope.component import getUtility

import unittest


name = 'Pinterest'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.plugins = dict(getUtilitiesFor(IPlugin))

    def test_plugin_available(self):
        self.assertIn(name, self.plugins)

    def test_plugin_config(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.name, name)
        self.assertEqual(plugin.id, 'pinterest')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.config_view())

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@pinterest-plugin')

    def test_plugin_metadata(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.metadata())

    def test_plugin_plugin(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.plugin(), 'plugin')


class PluginViewsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                self.portal, type='News Item', title='foo')
            set_image_field(self.newsitem, load_image(1024, 768), 'image/png')

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        plugin_view = self.plugin.view()
        view = self.newsitem.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('js/pinit.js', html)
        self.assertIn('pin_it_button.png', html)

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Pin it!', html)

    def test_plugin_view_newsitem(self):
        plugin_view = self.plugin.view()
        view = self.newsitem.restrictedTraverse(plugin_view)

        # At news item, use image field
        expected = r'http://nohost/plone/foo/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(view.image_url(), expected)

    def test_plugin_view_image(self):
        with api.env.adopt_roles(['Manager']):
            image = api.content.create(
                self.portal, type='Image', title='bar')
            set_image_field(image, load_image(1024, 768), 'image/png')

        plugin_view = self.plugin.view()
        view = image.restrictedTraverse(plugin_view)

        # At image, use local image
        expected = r'http://nohost/plone/bar/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(view.image_url(), expected)

    def test_plugin_view_document(self):
        with api.env.adopt_roles(['Manager']):
            document = api.content.create(
                self.portal, type='Document', title='baz')

        plugin_view = self.plugin.view()
        view = document.restrictedTraverse(plugin_view)

        # At document, return logo
        image_url = view.image_url()
        self.assertIn('logo.png', image_url)

    def test_plugin_view_pin_count(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.pin_count(), 'beside')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        self.assertEqual(view.pin_count(), 'above')
