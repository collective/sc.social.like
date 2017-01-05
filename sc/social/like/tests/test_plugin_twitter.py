# -*- coding: utf-8 -*-
from plone import api
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
        alsoProvides(self.layer['request'], ISocialLikeLayer)

        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                self.portal,
                type='News Item',
                title='Lorem Ipsum',
                description='Neque Porro',
            )
        set_image_field(self.newsitem, load_image(1024, 768), 'image/png')

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view_metadata(self):

        def get_meta_content(name):
            """Return the content attribute of the meta tag specified by name."""
            return html.find('*/meta[@name="{0}"]'.format(name)).attrib['content']

        view = self.newsitem.restrictedTraverse(self.plugin.view())
        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        api.portal.set_registry_record(record, 'plone')

        from lxml import etree
        html = etree.HTML(view.metadata())

        self.assertEqual(get_meta_content('twitter:card'), 'summary_large_image')
        expected = r'http://nohost/plone/lorem-ipsum/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(get_meta_content('twitter:image'), expected)
        self.assertEqual(get_meta_content('twitter:site'), '@plone')
        self.assertEqual(get_meta_content('twitter:title'), 'Lorem Ipsum')
        self.assertEqual(get_meta_content('twitter:description'), 'Neque Porro')

    def test_plugin_view_html(self):
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('twitter-share-button', html)

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        view = self.portal.restrictedTraverse(self.plugin.view())
        html = view.link()
        self.assertIn('Tweet it!', html)

    def test_plugin_twitter_username(self):
        self.settings.twitter_username = '@simplesconsult'

        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('data-via="@simplesconsult"', html)

    def test_plugin_urlnoscript_encoding(self):
        self.newsitem.setTitle(u'Notícia')
        self.settings.twitter_username = '@simplesconsult'

        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('%20via%20%40simplesconsult">Tweet', html)

    def test_plugin_language(self):
        self.newsitem.setLanguage('pt-br')
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('data-lang="pt-br"', html)

        self.newsitem.setLanguage('en')
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        html = view.plugin()
        self.assertIn('data-lang="en"', html)

    def test_share_link(self):
        view = self.newsitem.restrictedTraverse(self.plugin.view())
        share_link = view.share_link
        self.assertTrue(share_link().endswith('text=Lorem+Ipsum'))

        # unicode
        self.newsitem.setTitle(u'¡Notícia de última hora!')
        self.assertTrue(share_link().endswith(
            'text=%C2%A1Not%C3%ADcia+de+%C3%BAltima+hora%21'))
