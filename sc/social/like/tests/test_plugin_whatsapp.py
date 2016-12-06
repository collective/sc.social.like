# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.whatsapp import browser
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest


name = 'WhatsApp'


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
        self.assertEqual(plugin.id, 'whatsapp')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.config_view())

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@whatsapp-plugin')

    def test_plugin_metadata(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.metadata(), 'metadata')

    def test_plugin_plugin(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.plugin(), 'plugin')


class PluginViewsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)
        alsoProvides(self.request, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def setup_content(self, portal):
        portal.invokeFactory('Document', 'my-document')
        self.document = portal['my-document']

    def test_plugin_view(self):
        plugin = self.plugin
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('whatsapp', html)

    def test_plugin_urlnoscript_encoding(self):
        plugin = self.plugin
        document = self.document
        document.setTitle(u'Notícia')

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn(
            'Not%C3%ADcia%20-%20http%3A//nohost/plone/my-document" class="whatsapp">Share', html)
