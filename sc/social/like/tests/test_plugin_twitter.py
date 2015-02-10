# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.controlpanel.likes import LikeControlPanelAdapter
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.twitter import browser
from sc.social.like.plugins.twitter import controlpanel
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest2 as unittest

name = 'Twitter'


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
        self.assertEqual(plugin.id, 'twitter')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.config_view(), '@@twitter-config')

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@twitter-plugin')

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
        self.adapter = LikeControlPanelAdapter(self.portal)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def setup_content(self, portal):
        portal.invokeFactory('Document', 'my-document')
        self.document = portal['my-document']

    def test_config_view(self):
        plugin = self.plugin
        portal = self.portal
        config_view = plugin.config_view()
        view = portal.restrictedTraverse(config_view)
        self.assertTrue(isinstance(view, controlpanel.ProviderControlPanel))

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
        self.assertIn('twitter-share-button', html)

    def test_plugin_twittvia(self):
        plugin = self.plugin
        document = self.document
        adapter = controlpanel.ControlPanelAdapter(self.portal)
        adapter.twittvia = u'@simplesconsult'

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('data-via="@simplesconsult"', html)

    def test_plugin_urlnoscript_encoding(self):
        plugin = self.plugin
        document = self.document
        document.setTitle(u'Notícia')
        adapter = controlpanel.ControlPanelAdapter(self.portal)
        adapter.twittvia = u'@simplesconsult'

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('%20via%20%40simplesconsult">Tweet', html)

    def test_plugin_language(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        self.document.setLanguage('pt-br')
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('data-lang="pt-br"', html)

        self.document.setLanguage('en')
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('data-lang="en"', html)
