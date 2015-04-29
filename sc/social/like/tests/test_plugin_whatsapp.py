# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.controlpanel.likes import LikeControlPanelAdapter
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.whatsapp import browser
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest2 as unittest

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

    def _set_mobile_browser(self, is_mobile):
        if is_mobile:
            self.request.environ['HTTP_USER_AGENT'] = (
                'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) '
                'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 '
                'Safari/6533.18.5'
            )
        else:
            del(self.request.environ['HTTP_USER_AGENT'])

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self._set_mobile_browser(True)
        self.adapter = LikeControlPanelAdapter(self.portal)
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
            'Not%C3%ADcia%20-%20http%3A//nohost/plone/my-document">Share in WhatsApp',
            html
        )

    def test_is_mobile(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)

        self._set_mobile_browser(False)
        self.assertFalse(view.is_mobile_browser())

        self._set_mobile_browser(True)
        self.assertTrue(view.is_mobile_browser())
