# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like import utils
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook import browser
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.plugins.facebook.utils import fix_iso
from sc.social.like.plugins.interfaces import IPlugin
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtilitiesFor
from zope.component import getUtility

import unittest


name = 'Facebook'


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

        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                self.portal, type='News Item', title='foo')

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

        self.plugins = dict(getUtilitiesFor(IPlugin))
        self.plugin = self.plugins[name]

    def test_plugin_view(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertTrue(isinstance(view, browser.PluginView))

    def test_plugin_view_html_likeonly(self):
        self.settings.fbbuttons = ('Like',)

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('fb-like', html)
        self.assertNotIn('fb-share-button', html)

    def test_plugin_view_html_shareonly(self):
        self.settings.fbbuttons = ('Share',)
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertNotIn('fb-like', html)
        self.assertIn('fb-share-button', html)

    def test_plugin_view_html_both(self):
        self.settings.fbbuttons = ('Like', 'Share')

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.plugin()
        self.assertIn('fb-like', html)
        self.assertIn('data-share', html)
        self.assertNotIn('fb-share-button', html)

    def test_privacy_plugin_view_html(self):
        self.settings.do_not_track = True

        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.link()
        # Check that an app_id is required
        self.assertEqual('', html.strip())
        self.settings.facebook_app_id = '12345'
        view = self.portal.restrictedTraverse(plugin_view)
        html = view.link()
        self.assertIn('Share on Facebook', html)

    # FIXME: we need to rethink this feature
    @unittest.skipIf(IS_PLONE_5, 'Metadata viewlet is disabled in Plone 5')
    def test_plugin_view_metadata(self):

        def get_meta_property(name):
            meta = html.find('*/meta[@property="{0}"]'.format(name))
            if meta is not None:
                return meta.attrib['content']

        view = self.newsitem.restrictedTraverse(self.plugin.view())
        self.settings.facebook_username = 'plone'
        self.settings.facebook_app_id = '1234567890'

        from lxml import etree
        html = etree.HTML(view.metadata())
        self.assertEqual(get_meta_property('fb:admins'), 'plone')
        self.assertEqual(get_meta_property('fb:app_id'), '1234567890')

    # FIXME: we need to rethink this feature
    @unittest.skipIf(IS_PLONE_5, 'Metadata viewlet is disabled in Plone 5')
    def test_plugin_language(self):
        plugin_view = self.plugin.view()
        self.newsitem.setLanguage('pt-br')
        view = self.newsitem.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertIn('connect.facebook.net/pt_BR/all.js', html)

        self.newsitem.setLanguage('en')
        view = self.newsitem.restrictedTraverse(plugin_view)
        html = view.metadata()
        self.assertIn('connect.facebook.net/en_GB/all.js', html)

    def test_plugin_view_typebutton(self):
        plugin_view = self.plugin.view()
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton(), 'button_count')
        self.assertEqual(view.width, '90px')

        # Change to vertical
        self.settings.typebutton = 'vertical'
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton(), 'box_count')
        self.assertEqual(view.width, '55px')

        # disable show number of likes on vertical
        self.settings.typebutton = 'vertical'
        self.settings.fbshowlikes = False
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton(), 'button')
        self.assertEqual(view.width, '55px')

        # horizontal without numbers is also button
        self.settings.typebutton = 'horizontal'
        self.settings.fbshowlikes = False
        view = self.portal.restrictedTraverse(plugin_view)
        self.assertEqual(view.typebutton(), 'button')
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
