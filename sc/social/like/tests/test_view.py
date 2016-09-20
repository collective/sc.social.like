# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.browser.socialikes import SocialLikes
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.testing import INTEGRATION_TESTING
from zope.interface import alsoProvides

import unittest


class BrowserViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
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
