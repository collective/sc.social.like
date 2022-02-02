# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.component import getUtility

import unittest


name = 'Twitter'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.plugins = dict(getUtilitiesFor(IPlugin))

    def test_plugin_available(self):
        self.assertIn(name, self.plugins)

    def test_plugin_config(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.name, name)
        self.assertEqual(plugin.id, 'twitter')

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

        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                self.portal, type='News Item', title='foo')

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view_html(self):
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('twitter-share-button', html)

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        view = self.portal.restrictedTraverse(self.plugin.view())
        html = view.link()
        self.assertIn('Tweet', html)

    def test_plugin_twitter_username(self):
        self.settings.twitter_username = 'simplesconsult'
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('data-via="simplesconsult"', html)

    def test_share_link(self):
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        share_link = view.share_link
        got = share_link()
        want = 'text=foo'
        self.assertTrue(want in got, '%r not in %r' % (want, got))  # noqa: S001

        # unicode
        self.newsitem.setTitle('¡Notícia de última hora!')
        got = share_link()
        want = 'text=%C2%A1Not%C3%ADcia+de+%C3%BAltima+hora%21'
        self.assertTrue(want in got, '%r not in %r' % (want, got))  # noqa: S001
