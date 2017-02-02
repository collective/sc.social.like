# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sc.social.like.browser.viewlets import SocialLikesViewlet
from sc.social.like.browser.viewlets import SocialMetadataViewlet
from sc.social.like.interfaces import ISocialLikeLayer
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING
from zope.interface import alsoProvides

import unittest


do_not_track = ISocialLikeSettings.__identifier__ + '.do_not_track'


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
        try:
            html = self.document.atct_edit()  # Archetypes
        except AttributeError:
            html = self.document.restrictedTraverse('@@edit')()  # Dexterity
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
        api.content.transition(obj=self.document, transition='publish')

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
        try:
            html = self.document.atct_edit()  # Archetypes
        except AttributeError:
            html = self.document.restrictedTraverse('@@edit')()  # Dexterity
        self.assertNotIn('id="viewlet-social-like"', html)

    def test_render(self):
        viewlet = self.viewlet(self.document)
        html = viewlet.render()
        self.assertIn('id="viewlet-social-like"', html)
        self.assertIn('class="horizontal"', html)

    def test_rendermethod_default(self):
        viewlet = self.viewlet(self.document)
        self.assertEqual(viewlet.render_method, 'plugin')

    def test_rendermethod_privacy(self):
        api.portal.set_registry_record(do_not_track, True)
        viewlet = self.viewlet(self.document)
        self.assertEqual(viewlet.render_method, 'link')

    def test_rendermethod_privacy_opt_cookie(self):
        api.portal.set_registry_record(do_not_track, False)
        self.request.cookies['social-optout'] = 'true'
        viewlet = self.viewlet(self.document)
        self.assertEqual(viewlet.render_method, 'link')

    def test_rendermethod_privacy_donottrack(self):
        api.portal.set_registry_record(do_not_track, False)
        self.request.environ['HTTP_DNT'] = '1'
        viewlet = self.viewlet(self.document)
        self.assertEqual(viewlet.render_method, 'link')
