# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


name = 'Twitter'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
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
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

        with api.env.adopt_roles(['Manager']):
            self.image = api.content.create(
                self.portal, 'Image', id='test-image')

        set_image_field(self.image, load_image(1024, 768), 'image/png')

    def setup_content(self, portal):
        portal.invokeFactory('Document', 'my-document')
        self.document = portal['my-document']

    def test_plugin_view_metadata(self):
        plugin = self.plugin
        image = self.image
        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)
        view.title = 'Twitter Title'
        view.description = 'Twitter Description'
        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        api.portal.set_registry_record(record, 'plone')

        metadata = view.metadata()
        self.assertIn(
            '<meta name="twitter:card" content="summary_large_image" />', metadata)
        self.assertIn(
            '<meta name="twitter:image" content="http://nohost/plone/test-image/@@images', metadata)
        self.assertIn(
            '<meta name="twitter:site" content="@plone" />', metadata)
        self.assertIn(
            '<meta name="twitter:title" content="Twitter Title" />', metadata)
        self.assertIn(
            '<meta name="twitter:description" content="Twitter Description" />', metadata)

    def test_plugin_view_html(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('twitter-share-button', html)

    def test_privacy_plugin_view_html(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.do_not_track = True

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Tweet it!', html)

    def test_plugin_twitter_username(self):
        plugin = self.plugin
        document = self.document
        self.settings.twitter_username = '@simplesconsult'

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('data-via="@simplesconsult"', html)

    def test_plugin_urlnoscript_encoding(self):
        plugin = self.plugin
        document = self.document
        document.setTitle(u'Notícia')
        self.settings.twitter_username = '@simplesconsult'

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
