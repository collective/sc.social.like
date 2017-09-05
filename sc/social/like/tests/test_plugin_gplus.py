# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.gplus import browser
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.component import getUtility

import unittest


name = 'Google+'


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
        self.assertEqual(plugin.id, 'gplus')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertIsNone(plugin.config_view())

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@gplus-plugin')

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

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def setup_content(self, portal):
        portal.invokeFactory('Document', 'my-document')
        self.document = portal['my-document']

    def test_plugin_view(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        from lxml import etree
        plugin_view = self.plugin.view()
        view = self.document.restrictedTraverse(plugin_view)
        html = etree.HTML(view.plugin())
        script = html.find('*/script')
        self.assertEqual(script.attrib['src'], 'https://apis.google.com/js/platform.js')
        div = html.find('*/div')
        self.assertEqual(div.attrib['data-href'], 'http://nohost/plone/my-document')
        self.assertEqual(div.attrib['data-annotation'], 'bubble')

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Share on Google+', html)

    def test_plugin_view_annotation(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.annotation(), 'bubble')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        self.assertEqual(view.annotation(), 'vertical-bubble')
