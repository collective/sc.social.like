# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.config import PROJECTNAME
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'sociallikes-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        from plone.app.testing import logout
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@sociallikes-settings')

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


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_enabled_portal_types_record(self):
        record = 'sc.social.like.enabled_portal_types'
        self.assertEqual(
            api.portal.get_registry_record(record),
            ('Document', 'Event', 'News Item', 'File')
        )

    def test_plugins_enabled_record(self):
        record = 'sc.social.like.plugins_enabled'
        self.assertEqual(
            api.portal.get_registry_record(record), None)  # FIXME

    def test_typebutton_record(self):
        record = 'sc.social.like.typebutton'
        self.assertEqual(
            api.portal.get_registry_record(record), u'horizontal')

    def test_do_not_track_record(self):
        record = 'sc.social.like.do_not_track'
        self.assertFalse(api.portal.get_registry_record(record))

    def test_records_removed_on_uninstall(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry

        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        registry = getUtility(IRegistry)
        unexpected = (
            'sc.social.like.enabled_portal_types',
            'sc.social.like.plugins_enabled',
            'sc.social.like.typebutton',
            'sc.social.like.do_not_track',
        )
        self.assertNotIn(unexpected, registry.records)
