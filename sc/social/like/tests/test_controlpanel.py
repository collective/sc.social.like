# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import get_installer
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = api.content.get_view('sociallike-settings', self.portal, self.request)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@sociallike-settings')

    def test_controlpanel_installed(self):
        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertIn('sociallikes', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = get_installer(self.portal, self.request)

        with api.env.adopt_roles(['Manager']):
            qi.uninstall_product(PROJECTNAME)

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('sociallikes', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

    def test_enabled_portal_types_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enabled_portal_types'))
        self.assertEqual(
            self.settings.enabled_portal_types,
            ('Document', 'Event', 'News Item'),
        )

    def test_plugins_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'plugins_enabled'))
        self.assertEqual(
            self.settings.plugins_enabled, ('Facebook', 'Twitter'))

    def test_validation_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'validation_enabled'))
        self.assertTrue(self.settings.validation_enabled)

    def test_typebutton_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'typebutton'))
        self.assertEqual(self.settings.typebutton, 'horizontal')

    def test_do_not_track_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'do_not_track'))
        self.assertFalse(self.settings.do_not_track)

    def test_fallback_image_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'fallback_image'))
        self.assertEqual(self.settings.fallback_image, None)

    def test_fbaction_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'fbaction'))
        self.assertEqual(self.settings.fbaction, 'like')

    def test_facebook_username_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'facebook_username'))
        self.assertEqual(self.settings.facebook_username, '')

    def test_facebook_app_id_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'facebook_app_id'))
        self.assertEqual(self.settings.facebook_app_id, '')

    def test_fbbuttons_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'fbbuttons'))
        self.assertEqual(self.settings.fbbuttons, ('Like',))

    def test_fbshowlikes_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'fbshowlikes'))
        self.assertEqual(self.settings.fbshowlikes, True)

    def test_twitter_username_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'twitter_username'))
        self.assertEqual(self.settings.twitter_username, '')

    def test_facebook_prefetch_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'facebook_prefetch_enabled'))
        self.assertEqual(self.settings.facebook_prefetch_enabled, False)

    def test_folderish_templates_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'folderish_templates'))
        self.assertEqual(self.settings.folderish_templates, None)

    def test_records_removed_on_uninstall(self):
        qi = get_installer(self.portal, self.request)

        with api.env.adopt_roles(['Manager']):
            qi.uninstall_product(PROJECTNAME)

        records = [
            ISocialLikeSettings.__identifier__ + '.enabled_portal_types',
            ISocialLikeSettings.__identifier__ + '.plugins_enabled',
            ISocialLikeSettings.__identifier__ + '.validation_enabled',
            ISocialLikeSettings.__identifier__ + '.typebutton',
            ISocialLikeSettings.__identifier__ + '.do_not_track',
            ISocialLikeSettings.__identifier__ + '.canonical_domain',
            ISocialLikeSettings.__identifier__ + '.fallback_image',
            ISocialLikeSettings.__identifier__ + '.fbaction',
            ISocialLikeSettings.__identifier__ + '.facebook_username',
            ISocialLikeSettings.__identifier__ + '.facebook_app_id',
            ISocialLikeSettings.__identifier__ + '.fbbuttons',
            ISocialLikeSettings.__identifier__ + '.fbshowlikes',
            ISocialLikeSettings.__identifier__ + '.twitter_username',
            ISocialLikeSettings.__identifier__ + '.facebook_prefetch_enabled',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
