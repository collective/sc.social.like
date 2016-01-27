# -*- coding: utf-8 -*-
from plone.browserlayer.utils import registered_layers
from sc.social.like.config import PROJECTNAME
from sc.social.like.testing import INTEGRATION_TESTING

import unittest

JAVASCRIPTS = [
]

CSS = [
    '++resource++sl_stylesheets/social_like.css',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_portal_properties(self):
        self.assertTrue(api.portal.get_registry_record('sc.social.like.enabled_portal_types'))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ISocialLikeLayer', layers)

    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JAVASCRIPTS:
            self.assertIn(id, resource_ids, '%s not installed' % id)

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertIn(id, resource_ids, '%s not installed' % id)


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

    def test_portal_properties_removed(self):
        portal_properties = self.portal['portal_properties']
        self.assertNotIn('sc_social_likes_properties', portal_properties)

    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JAVASCRIPTS:
            self.assertNotIn(id, resource_ids, '%s not removed' % id)

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertNotIn(id, resource_ids, '%s not removed' % id)
