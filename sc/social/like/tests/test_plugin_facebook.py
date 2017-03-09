# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from sc.social.like import utils
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook import browser
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.plugins.facebook.utils import fix_iso
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


name = 'Facebook'


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
        self.assertEqual(plugin.id, 'facebook')

    def test_plugin_view(self):
        plugin = self.plugins[name]
        self.assertEqual(plugin.view(), '@@facebook-plugin')

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
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.setup_content(self.portal)

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def setup_content(self, portal):
        portal.invokeFactory('Document', 'my-document')
        portal.invokeFactory('News Item', 'my-newsitem')
        portal.invokeFactory('Image', 'my-image')
        self.document = portal['my-document']
        self.newsitem = portal['my-newsitem']
        set_image_field(self.newsitem, load_image(1024, 768), 'image/png')
        self.image = portal['my-image']
        set_image_field(self.image, load_image(1024, 768), 'image/png')

    def test_plugin_view(self):
        plugin = self.plugin
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html_likeonly(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.fbbuttons = ('Like',)

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('fb-like', html)
        self.assertNotIn('fb-share-button', html)

    def test_plugin_view_html_shareonly(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.fbbuttons = ('Share',)

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertNotIn('fb-like', html)
        self.assertIn('fb-share-button', html)

    def test_plugin_view_html_both(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.fbbuttons = ('Like', 'Share')

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('fb-like', html)
        self.assertIn('data-share', html)
        self.assertNotIn('fb-share-button', html)

    def test_privacy_plugin_view_html(self):
        plugin = self.plugin
        portal = self.portal
        self.settings.do_not_track = True

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        html = view.link()
        # Check that an app_id is required
        self.assertEqual('', html.strip())
        self.settings.facebook_app_id = '12345'
        view = portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Share on Facebook', html)

    def test_plugin_view_metadata(self):
        plugin = self.plugin
        portal = self.portal
        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)

        metadata = view.metadata()
        self.assertIn('og:site_name', metadata)

        # At root, use site logo
        image_url = view.image_url()
        self.assertIn('logo.png', image_url)

        # At root, use website type
        og_type = view.type()
        self.assertIn('website', og_type)

    def test_plugin_view_document(self):
        plugin = self.plugin
        document = self.document
        portal = self.portal

        plugin_view = plugin.view()
        view = document.restrictedTraverse(plugin_view)

        # At document, use site logo
        image_url = view.image_url()
        self.assertIn('logo.png', image_url)

        # At document, use article type
        og_type = view.type()
        self.assertIn('article', og_type)

        # At document, default page of portal, use website type
        portal.setDefaultPage(document.id)
        og_type = view.type()
        self.assertIn('website', og_type)

    def test_plugin_view_image(self):
        plugin = self.plugin
        image = self.image

        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)

        # At image, use local image
        image_url = view.image_url()
        self.assertNotIn('logo.png', image_url)
        self.assertEqual(view.image_width(), 1024)
        self.assertEqual(view.image_height(), 768)
        self.assertEqual(view.image_type(), 'image/png')

        # XXX: avoid failures because of unchanged modification date
        #      this happens only on Dexterity-based content types
        from time import sleep
        sleep(1)

        # Set a larger image
        set_image_field(image, load_image(1920, 1080), 'image/png')

        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)
        self.assertEqual(view.image_width(), 1200)
        self.assertEqual(view.image_height(), 675)

    def test_plugin_view_image_large(self):
        plugin = self.plugin
        image = self.image
        set_image_field(image, load_image(1920, 1080), 'image/png')

        plugin_view = plugin.view()
        view = image.restrictedTraverse(plugin_view)

        # At newsitem, use image
        image_url = view.image_url()
        self.assertNotIn('logo.png', image_url)

        self.assertEqual(view.image_width(), 1200)
        self.assertEqual(view.image_height(), 675)

    def test_plugin_view_newsitem(self):
        plugin = self.plugin
        newsitem = self.newsitem

        plugin_view = plugin.view()
        view = newsitem.restrictedTraverse(plugin_view)

        # At newsitem, use image
        image_url = view.image_url()
        self.assertNotIn('logo.png', image_url)
        self.assertEqual(view.image_width(), 1024)
        self.assertEqual(view.image_height(), 768)

    def test_plugin_view_newsitem_large(self):
        plugin = self.plugin
        newsitem = self.newsitem
        set_image_field(newsitem, load_image(1920, 1080), 'image/png')

        plugin_view = plugin.view()
        view = newsitem.restrictedTraverse(plugin_view)

        # At newsitem, use image
        image_url = view.image_url()
        self.assertNotIn('logo.png', image_url)

        self.assertEqual(view.image_width(), 1200)
        self.assertEqual(view.image_height(), 675)

    def test_plugin_language(self):
        plugin = self.plugin
        document = self.document
        plugin_view = plugin.view()
        self.document.setLanguage('pt-br')
        view = document.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertIn('connect.facebook.net/pt_BR/all.js', html)

        self.document.setLanguage('en')
        view = document.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertIn('connect.facebook.net/en_GB/all.js', html)

    def test_plugin_view_typebutton(self):
        portal = self.portal
        plugin = self.plugin

        plugin_view = plugin.view()
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'button_count')
        self.assertEqual(view.width, '90px')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'box_count')
        self.assertEqual(view.width, '55px')

        # disable show number of likes on vertical
        self.settings.typebutton = 'vertical'
        self.settings.fbshowlikes = False
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'button')
        self.assertEqual(view.width, '55px')

        # horizontal without numbers is also button
        self.settings.typebutton = 'horizontal'
        self.settings.fbshowlikes = False
        view = portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton, 'button')
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
        self.assertEqual(facebook_language(['pt-br', 'pt'], default), 'pt_BR')
        self.assertEqual(facebook_language(['de', ], default), 'de_DE')
        self.assertEqual(facebook_language(['it', ], default), 'it_IT')
        self.assertEqual(facebook_language(['fi', 'en'], default), 'fi_FI')
        self.assertEqual(facebook_language(['ga', ], default), 'ga_IE')
        self.assertEqual(facebook_language(['ji', ], default), default)
        self.assertEqual(facebook_language([], default), default)


class ImageResizingTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_larger_width_height(self):
        current = (1920, 1080)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 1200)
        self.assertEqual(height, 675)

    def test_larger_width_height_small_aspect(self):
        current = (1920, 1920)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

    def test_larger_width(self):
        current = (1210, 400)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 1210)
        self.assertEqual(height, 400)

    def test_larger_height(self):
        current = (800, 800)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 800)
        self.assertEqual(height, 800)

    def test_smaller_width(self):
        current = (640, 640)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 640)
        self.assertEqual(height, 640)

    def test_smaller_height(self):
        current = (800, 600)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 800)
        self.assertEqual(height, 600)

    def test_smaller_resized_height(self):
        current = (1220, 632)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 1216)
        self.assertEqual(height, 630)

    def test_width_height_zero(self):
        current = (0, 0)
        new = (1200, 630)
        width, height = utils._image_size(current, new)
        self.assertEqual(width, 0)
        self.assertEqual(height, 0)
