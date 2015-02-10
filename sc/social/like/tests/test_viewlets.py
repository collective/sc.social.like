# -*- coding: utf-8 -*-
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.browser.viewlets import SocialLikesViewlet
from sc.social.like.browser.viewlets import SocialMetadataViewlet
from sc.social.like.interfaces import ISocialLikeLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest2 as unittest


class MetadataViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'my-document')
        self.document = self.portal['my-document']

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = SocialMetadataViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_disabled_on_portal(self):
        viewlet = self.viewlet(self.portal)
        self.assertFalse(viewlet.enabled())

    def test_enabled_on_portal_with_template_full_view(self):
        # Set layout to folder_full_view
        self.portal.setLayout('folder_full_view')
        viewlet = self.viewlet(self.portal)
        self.assertTrue(viewlet.enabled())

    def test_enabled_on_document(self):
        viewlet = self.viewlet(self.document)
        self.assertTrue(viewlet.enabled())

    def test_disabled_on_edit_document(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', self.document.absolute_url() + '/edit')
        html = self.document.atct_edit()
        self.assertNotIn('og:site_name', html)

    def test_render(self):
        viewlet = self.viewlet(self.document)
        html = viewlet.render()
        self.assertGreater(len(html), 0)


class LikeViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.portal.REQUEST, ISocialLikeLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'my-document')
        self.document = self.portal['my-document']

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = SocialLikesViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_disabled_on_portal(self):
        viewlet = self.viewlet(self.portal)
        self.assertFalse(viewlet.enabled())

    def test_enabled_on_document(self):
        viewlet = self.viewlet(self.document)
        self.assertTrue(viewlet.enabled())

    def test_disabled_on_edit_document(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', self.document.absolute_url() + '/edit')
        html = self.document.atct_edit()
        self.assertNotIn('id="viewlet-social-like"', html)

    def test_render(self):
        viewlet = self.viewlet(self.document)
        html = viewlet.render()
        self.assertIn('id="viewlet-social-like"', html)
        self.assertIn('class="horizontal"', html)
