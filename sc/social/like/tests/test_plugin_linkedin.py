# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.plugins.linkedin import browser
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.component import getUtility

import unittest


name = 'LinkedIn'


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

        with api.env.adopt_roles(['Manager']):
            self.document = api.content.create(
                self.portal, type='Document', title='foo')

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        from lxml import etree
        plugin_view = self.plugin.view()
        view = self.document.restrictedTraverse(plugin_view)
        html = etree.HTML(view.plugin())
        scripts = html.findall('*/script')
        self.assertEqual(scripts[0].attrib['src'], '//platform.linkedin.com/in.js')
        self.assertEqual(scripts[1].attrib['type'], 'IN/Share')
        self.assertEqual(scripts[1].attrib['data-counter'], 'right')
        self.assertEqual(scripts[1].attrib['data-url'], 'http://nohost/plone/foo')

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Share on Linkedin', html)

    def test_plugin_view_typebutton(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.counter(), 'right')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        self.assertEqual(view.counter(), 'top')
