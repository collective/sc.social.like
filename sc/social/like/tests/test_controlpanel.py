# -*- coding: utf-8 -*-
from plone.app.testing import logout
from Products.CMFCore.utils import getToolByName
from sc.social.like.controlpanel.likes import LikeControlPanelAdapter
from sc.social.like.controlpanel.likes import ProvidersControlPanel
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter

import unittest2 as unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.adapter = LikeControlPanelAdapter(self.portal)
        self.sheet = self.portal.portal_properties.sc_social_likes_properties

    def test_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name='likes-providers')
        view = view.__of__(self.portal)
        self.assertTrue(view())
        self.assertTrue(isinstance(view, ProvidersControlPanel))

    def test_controlpanel_plugins_configs(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name='likes-providers')
        configs = view.plugins_configs()
        self.assertEqual(len(configs), 2)

    def test_controlpanel_view_protected(self):
        # control panel view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@likes-providers')

    def test_configlet_install(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        self.assertIn('sociallikes', installed)

    def test_enabled_portal_types(self):
        adapter = self.adapter
        adapter.enabled_portal_types = ()
        self.assertEqual(len(adapter.enabled_portal_types), 0)
        adapter.enabled_portal_types = ('Document', 'Event')

        self.assertEqual(len(adapter.enabled_portal_types), 2)
        self.assertEqual(
            adapter.enabled_portal_types, self.sheet.enabled_portal_types)

    def test_plugins_enabled(self):
        adapter = self.adapter
        adapter.plugins_enabled = ()
        self.assertEqual(len(adapter.plugins_enabled), 0)
        adapter.plugins_enabled = ('Facebook', 'Twitter')

        self.assertEqual(len(adapter.plugins_enabled), 2)
        self.assertEqual(adapter.plugins_enabled, self.sheet.plugins_enabled)

    def test_typebutton(self):
        adapter = self.adapter
        adapter.typebutton = 'horizontal'
        self.assertEqual(adapter.typebutton, self.sheet.typebutton)

        adapter.typebutton = 'vertical'
        self.assertEqual(adapter.typebutton, self.sheet.typebutton)
