# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.browser.socialikes import SocialLikes
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


class BrowserViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'my-document')
        self.document = self.portal['my-document']

    def view(self, context=None):
        context = context or self.portal
        view = SocialLikes(context, self.request)
        return view

    def test_disabled_on_portal(self):
        view = self.view(self.portal)
        self.assertFalse(view.enabled)

    def test_enabled_on_document(self):
        view = self.view(self.document)
        self.assertTrue(view.enabled)


class FallBackImageViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def set_fallback_image(self, filename):
        from sc.social.like.interfaces import ISocialLikeSettings
        from sc.social.like.tests.utils import get_file_b64encoded
        record = ISocialLikeSettings.__identifier__ + '.fallback_image'
        logo = get_file_b64encoded(filename)
        api.portal.set_registry_record(record, logo)

    def test_no_fall_back_image(self):
        view = api.content.get_view(
            'sociallike-fallback-image', self.portal, self.request)
        self.assertEqual(len(view()), 0)
        self.assertEqual(self.request.RESPONSE.getStatus(), 410)

    def test_fall_back_image(self):
        self.set_fallback_image('imgtest_1920x1080.png')
        view = api.content.get_view(
            'sociallike-fallback-image', self.portal, self.request)
        self.assertEqual(len(view()), 42901)
        self.assertEqual(self.request.RESPONSE.getStatus(), 200)
        self.assertEqual(
            self.request.RESPONSE.getHeader('Cache-Control'),
            'max-age=120, public',
        )
