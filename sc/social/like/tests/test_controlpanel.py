# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import logout
from sc.social.like.config import PROJECTNAME
# from sc.social.like.controlpanel.likes import LikeControlPanelAdapter
# from sc.social.like.controlpanel.likes import ProvidersControlPanel
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter

import unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        # self.adapter = LikeControlPanelAdapter(self.portal)

    # def test_controlpanel_view(self):
    #     view = getMultiAdapter(
    #         (self.portal, self.portal.REQUEST), name='likes-providers')
    #     view = view.__of__(self.portal)
    #     self.assertTrue(view())
    #     # self.assertTrue(isinstance(view, ProvidersControlPanel))

    # def test_controlpanel_plugins_configs(self):
    #     view = getMultiAdapter(
    #         (self.portal, self.portal.REQUEST), name='likes-providers')
    #     configs = view.plugins_configs()
    #     self.assertEqual(len(configs), 2)

    # def test_controlpanel_view_protected(self):
    #     # control panel view can not be accessed by anonymous users
    #     from AccessControl import Unauthorized
    #     logout()
    #     with self.assertRaises(Unauthorized):
    #         self.portal.restrictedTraverse('@@likes-providers')

    def test_configlet_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('sociallikes', actions)

    def test_configlet_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('sociallikes', actions)

    # def test_enabled_portal_types(self):
    #     adapter = self.adapter
    #     adapter.enabled_portal_types = ()
    #     self.assertEqual(len(adapter.enabled_portal_types), 0)
    #     adapter.enabled_portal_types = ('Document', 'Event')
    #     enabled_portal_types = api.portal.get_registry_record('sc.social.like.enabled_portal_types')
    #     self.assertEqual(len(adapter.enabled_portal_types), 2)
    #     self.assertEqual(
    #         adapter.enabled_portal_types, enabled_portal_types)

    # def test_plugins_enabled(self):
    #     adapter = self.adapter
    #     adapter.plugins_enabled = ()
    #     self.assertEqual(len(adapter.plugins_enabled), 0)
    #     adapter.plugins_enabled = ('Facebook', 'Twitter')
    #     plugins_enabled = api.portal.get_registry_record('sc.social.like.plugins_enabled')
    #     self.assertEqual(len(adapter.plugins_enabled), 2)
    #     self.assertEqual(adapter.plugins_enabled, plugins_enabled)

    def test_typebutton(self):
        adapter = self.adapter
        adapter.typebutton = 'horizontal'
        typebutton = api.portal.get_registry_record('sc.social.like.typebutton')
        self.assertEqual(adapter.typebutton, typebutton)

        adapter.typebutton = 'vertical'
        self.assertEqual(adapter.typebutton, typebutton)
