# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.controlpanel.likes import LikeControlPanelAdapter
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.plugins.facebook import browser
from sc.social.like.plugins.facebook import controlpanel
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.plugins.facebook.utils import fix_iso
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import generate_image
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.interface import alsoProvides

import unittest2 as unittest

name = 'Facebook'


class PluginTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))

    def test_plugin_available(self):
        self.assertTrue(name in self.plugins)

    def test_plugin_config(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.name, name)
        self.assertEqual(plugin.id, 'facebook')

    def test_plugin_config_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.config_view(),
                         '@@facebook-config')

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(),
                         '@@facebook-plugin')

    def test_plugin_metadata(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.metadata(),
                         'metadata')

    def test_plugin_plugin(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.plugin(),
                         'plugin')


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
        portal.invokeFactory('News Item', 'my-newsitem')
        portal.invokeFactory('Image', 'my-image')
        self.document = portal['my-document']
        self.newsitem = portal['my-newsitem']
        self.newsitem.setImage(generate_image(1024, 768))
        self.image = portal['my-image']
        self.image.setImage(generate_image(1024, 768))

    def image_url(self, obj, field='image', scale='large'):

        view = obj.unrestrictedTraverse('@@images')
        scale = view.scale(fieldname='image', scale='large')
        return scale.url

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
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertTrue('fb-like' in html)

    def test_plugin_view_metadata(self):
        plugin = self.plugin
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)

        metadata = view.metadata()
        self.assertTrue('og:site_name' in metadata)

        # At root, use site logo
        image_url = view.image_url()
        self.assertTrue('logo.png' in image_url)

    def test_plugin_view_document(self):
        plugin = self.plugin
        document = self.document

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)

        # At document, use site logo
        image_url = view.image_url()
        self.assertTrue('logo.png' in image_url)

    def test_plugin_view_image(self):
        plugin = self.plugin
        image = self.image
        expected = self.image_url(image)

        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)

        # At image, use local image
        image_url = view.image_url()
        self.assertEqual(expected, image_url)

    def test_plugin_view_newsitem(self):
        plugin = self.plugin
        newsitem = self.newsitem
        expected = self.image_url(newsitem)

        plugin_view = plugin.view()
        view = newsitem.restrictedTraverse(plugin_view)

        # At newsitem, use image
        image_url = view.image_url()
        self.assertEqual(expected, image_url)

    def test_plugin_language(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        self.document.REQUEST['HTTP_ACCEPT_LANGUAGE'] = 'pt-br;q=0.5'
        view = document.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertTrue('connect.facebook.net/pt_BR/all.js' in html)

        self.document.REQUEST['HTTP_ACCEPT_LANGUAGE'] = 'en;q=0.5'
        view = document.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertTrue('connect.facebook.net/en_GB/all.js' in html)

    def test_plugin_view_typebutton(self):
        portal = self.portal
        plugin = self.plugin

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.button, 'button_count')
        self.assertEqual(view.typebutton, 'button_count')
        self.assertEqual(view.width, '90px')

        # Change to vertical
        adapter = self.adapter
        adapter.typebutton = 'vertical'
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'box_count')
        self.assertEqual(view.width, '55px')


class LanguageCodeTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_fix_iso(self):
        self.assertEqual(fix_iso('pt-br'), 'pt_BR')
        self.assertEqual(fix_iso('pt-pt'), 'pt_PT')
        self.assertEqual(fix_iso('en-gb'), 'en_GB')
        self.assertEqual(fix_iso('es-es'), 'es_ES')
        self.assertEqual(fix_iso('es-ar'), 'es_LA')
        self.assertEqual(fix_iso('es-cl'), 'es_LA')
        self.assertEqual(fix_iso('ar-sa'), 'ar_AR')
        self.assertEqual(fix_iso('ar-eg'), 'ar_AR')
        self.assertEqual(fix_iso('pt'), 'pt_PT')
        self.assertEqual(fix_iso('de'), 'de_DE')
        self.assertEqual(fix_iso('it'), 'it_IT')
        self.assertEqual(fix_iso('en'), 'en_GB')

    def test_facebook_language(self):
        default = 'en_US'
        self.assertEqual(facebook_language(['pt-br', 'pt'], default),
                         'pt_BR')
        self.assertEqual(facebook_language(['de', ], default),
                         'de_DE')
        self.assertEqual(facebook_language(['it', ], default),
                         'it_IT')
        self.assertEqual(facebook_language(['fi', 'en'], default),
                         'fi_FI')
        self.assertEqual(facebook_language(['ga', ], default),
                         'ga_IE')
        self.assertEqual(facebook_language(['ji', ], default),
                         default)
        self.assertEqual(facebook_language([], default),
                         default)
