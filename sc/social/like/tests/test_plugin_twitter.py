# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.config import IS_PLONE_5
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

    # FIXME: we need to rethink this feature
    @unittest.skipIf(IS_PLONE_5, 'Metadata viewlet is disabled in Plone 5')
    def test_plugin_view_metadata(self):

        def get_meta_content(name):
            """Return the content attribute of the meta tag specified."""
            meta = html.find('*/meta[@name="{0}"]'.format(name))
            if meta is not None:
                return meta.attrib['content']
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        api.portal.set_registry_record(record, 'plone')

        from lxml import etree
        html = etree.HTML(view.metadata())
        self.assertEqual(get_meta_content('twitter:card'), 'summary_large_image')
        self.assertEqual(get_meta_content('twitter:site'), '@plone')

        # privacy settings
        self.assertIsNone(get_meta_content('twitter:dnt'))
        self.settings.do_not_track = True
        html = etree.HTML(view.metadata())
        self.assertEqual(get_meta_content('twitter:dnt'), 'on')

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
        self.assertTrue(share_link().endswith('text=foo'))

        # unicode
        self.newsitem.setTitle(u'¡Notícia de última hora!')
        self.assertTrue(share_link().endswith(
            'text=%C2%A1Not%C3%ADcia+de+%C3%BAltima+hora%21'))
