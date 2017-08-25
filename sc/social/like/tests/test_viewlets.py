# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from profilehooks import profile
from profilehooks import timecall
from sc.social.like.browser.viewlets import SocialLikesViewlet
from sc.social.like.browser.viewlets import SocialMetadataViewlet
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING

import contextlib
import unittest


do_not_track = ISocialLikeSettings.__identifier__ + '.do_not_track'


@contextlib.contextmanager
def capture():
    """A context manager to capture stdout and stderr.
    http://stackoverflow.com/a/10743550/644075
    """
    import sys
    from cStringIO import StringIO
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0], out[1] = out[0].getvalue(), out[1].getvalue()


class MetadataViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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

    # FIXME: we need to rethink this feature
    @unittest.skipIf(IS_PLONE_5, 'Plone 5 includes metadata by default')
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

    def test_render_timecall(self):
        # rendering the viewlet 100 times must take less than 100 ms
        viewlet = self.viewlet(self.document)

        @timecall(immediate=True)
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render(times=100)

        import re
        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, 0.1)

    def test_render_profile(self):
        # show rendering profile
        viewlet = self.viewlet(self.document)

        @profile
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        render(times=100)


class LikeViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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

    def test_render_timecall(self):
        # rendering the viewlet 100 times must take less than 100 ms
        viewlet = self.viewlet(self.document)

        @timecall(immediate=True)
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render(times=100)

        import re
        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, 0.1)

    def test_render_profile(self):
        # show rendering profile
        viewlet = self.viewlet(self.document)

        @profile
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        render(times=100)
