# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer.utils import registered_layers
from sc.social.like.config import IS_PLONE_5
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
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ISocialLikeLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertIn(JAVASCRIPT, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tiles(self):
        registered = api.portal.get_registry_record('plone.app.tiles')
        [self.assertIn(t, registered) for t in TILES]


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('ISocialLikeLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertNotIn(JAVASCRIPT, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tiles_removed(self):
        registered = api.portal.get_registry_record('plone.app.tiles')
        [self.assertNotIn(t, registered) for t in TILES]
