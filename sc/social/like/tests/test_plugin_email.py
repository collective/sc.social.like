# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.email import browser
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest


name = 'Email'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_available(self):
        self.assertIn(name, self.plugins)

    def test_plugin_config(self):
        self.assertEqual(self.plugin.name, name)
        self.assertEqual(self.plugin.id, 'email')

    def test_plugin_config_view(self):
        self.assertIsNone(self.plugin.config_view())

    def test_plugin_view(self):
        self.assertEqual(self.plugin.view(), '@@email-plugin')

    def test_plugin_metadata(self):
        self.assertEqual(self.plugin.metadata(), 'metadata')

    def test_plugin_plugin(self):
        self.assertEqual(self.plugin.plugin(), 'plugin')


class PluginViewsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, ISocialLikeLayer)

        with api.env.adopt_roles(['Manager']):
            self.document = api.content.create(
                self.portal,
                type='Document',
                title='Lorem Ipsum',
                description='Neque Porro',
            )

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view(self):
        view = self.document.restrictedTraverse(self.plugin.view())
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html(self):
        view = self.document.restrictedTraverse(self.plugin.view())

        from lxml import etree
        html = etree.HTML(view.plugin())
        a = html.find('*/a')

        self.assertEqual(
            a.attrib['href'], 'http://nohost/plone/lorem-ipsum/sendto_form')
        self.assertEqual(a.attrib['title'], 'Share by email')
        self.assertIn('pat-plone-modal', a.attrib['class'])
