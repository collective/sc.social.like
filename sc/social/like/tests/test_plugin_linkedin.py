# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.linkedin import browser
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


name = 'LinkedIn'


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
        self.assertEqual(plugin.id, 'linkedin')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.config_view())

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@linkedin-plugin')

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
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
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
        self.assertIn('in/share', html)

    def test_privacy_plugin_view_html(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.do_not_track = True

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Share on Linkedin', html)

    def test_plugin_view_metadata(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        metadata = view.metadata()
        self.assertIn('linkedin.com/in.js', metadata)

    def test_plugin_view_typebutton(self):
        portal = self.portal
        plugin = self.plugin

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'right')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'top')
