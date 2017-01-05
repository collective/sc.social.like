# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.pinterest import browser
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


name = 'Pinterest'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
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
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def setup_content(self, portal):
        portal.invokeFactory('News Item', 'my-newsitem')
        portal.invokeFactory('Image', 'my-image')
        self.newsitem = portal['my-newsitem']
        set_image_field(self.newsitem, load_image(1024, 768), 'image/png')
        self.image = portal['my-image']
        set_image_field(self.image, load_image(1024, 768), 'image/png')

    def test_plugin_view(self):
        plugin = self.plugin
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        plugin = self.plugin
        newsitem = self.newsitem
        plugin_view = plugin.view()
        view = newsitem.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('js/pinit.js', html)
        self.assertIn('pin_it_button.png', html)

    def test_privacy_plugin_view_html(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.do_not_track = True

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Pin it!', html)

    def test_plugin_view_image(self):
        plugin = self.plugin
        image = self.image

        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)

        # At image, use local image
        expected = r'http://nohost/plone/my-image/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(view.image_url(), expected)

    def test_plugin_view_newsitem(self):
        plugin = self.plugin
        newsitem = self.newsitem

        plugin_view = plugin.view()
        view = newsitem.restrictedTraverse(plugin_view)

        # At newsitem, use image
        expected = r'http://nohost/plone/my-newsitem/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(view.image_url(), expected)

    def test_plugin_view_document(self):
        plugin = self.plugin
        self.portal.invokeFactory('Document', 'my-document')
        document = self.portal['my-document']
        expected = 'logo.png'

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)

        # At document, return logo
        image_url = view.image_url()
        self.assertIn(expected, image_url)

    def test_plugin_view_typebutton(self):
        portal = self.portal
        plugin = self.plugin

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'beside')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'above')
