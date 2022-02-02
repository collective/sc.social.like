# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer.utils import registered_layers
from Products.CMFPlone.utils import get_installer
from sc.social.like.config import PROJECTNAME
from sc.social.like.config import TILES
from sc.social.like.testing import HAS_COVER
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


JAVASCRIPT = '++resource++sl_scripts/social_like.js'
CSS = '++resource++sl_stylesheets/social_like.css'


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = get_installer(self.portal)
        self.assertTrue(qi.is_product_installed(PROJECTNAME))

    def test_addon_layer(self):
        layers = [ly.getName() for ly in registered_layers()]
        self.assertIn('ISocialLikeLayer', layers)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tiles(self):
        registered = api.portal.get_registry_record('plone.app.tiles')
        [self.assertIn(t, registered) for t in TILES]


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = get_installer(self.portal)
        self.qi.uninstall_product(PROJECTNAME)

    def test_uninstalled(self):
        self.assertFalse(self.qi.is_product_installed(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [ly.getName() for ly in registered_layers()]
        self.assertNotIn('ISocialLikeLayer', layers)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tiles_removed(self):
        registered = api.portal.get_registry_record('plone.app.tiles')
        [self.assertNotIn(t, registered) for t in TILES]
