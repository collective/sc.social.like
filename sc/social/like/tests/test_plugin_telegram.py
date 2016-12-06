# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.telegram import PluginView
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest


name = 'Telegram'


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
        self.assertEqual(plugin.id, 'telegram')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.config_view())

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@telegram-plugin')

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
        alsoProvides(self.request, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

        with api.env.adopt_roles(['Manager']):
            self.document = api.content.create(
                self.portal, 'Document', 'my-document')

    def test_plugin_view(self):
        plugin = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin)
        self.assertTrue(isinstance(view, PluginView))

    def test_plugin_view_html(self):
        plugin = self.plugin.view()
        view = self.document.restrictedTraverse(plugin)
        html = view.plugin()
        self.assertIn('telegram', html)

    def test_plugin_urlnoscript_encoding(self):
        plugin = self.plugin.view()
        self.document.setTitle(u'Notícia')
        view = self.document.restrictedTraverse(plugin)
        html = view.plugin()
        self.assertIn(
            'http%3A//nohost/plone/my-document" class="telegram">Share', html)
