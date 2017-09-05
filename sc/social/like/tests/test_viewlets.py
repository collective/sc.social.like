# -*- coding: utf-8 -*-
from plone import api
from profilehooks import profile
from profilehooks import timecall
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field

import contextlib
import os
import re
import unittest


# TODO: document this on README
# set the "SKIP_CODE_PROFILING" environent variable to skip profiling
skip_profiling = os.environ.get('SKIP_CODE_PROFILING', False)

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


class ViewletBaseTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(
                self.portal, type='News Item', id='foo')
        set_image_field(self.obj, load_image(1024, 768), 'image/png')

    def _enable_all_plugins(self):
        from plone.registry.interfaces import IRegistry
        from sc.social.like.plugins.interfaces import IPlugin
        from zope.component import getUtilitiesFor
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialLikeSettings)
        all_plugins = tuple(i[0] for i in getUtilitiesFor(IPlugin))
        settings.plugins_enabled = all_plugins

    def _get_viewlet_by_name(self, name, context):
        from plone.app.customerize.registration import getViews
        from zope.publisher.interfaces.browser import IBrowserRequest
        from zope.viewlet.interfaces import IViewlet
        request = self.request
        registration = None
        for v in getViews(IBrowserRequest):
            if v.provided == IViewlet:
                if v.name == name:
                    registration = v

        if registration is None:
            raise ValueError

        viewlet = registration.factory(context, request, None, None).__of__(context)
        viewlet.update()
        return viewlet


class MetadataViewletTestCase(ViewletBaseTestCase):

    def viewlet(self, context):
        return self._get_viewlet_by_name('sc.social.likes_metadata', context)

    def test_metadata_viewlet_is_disabled_on_portal(self):
        viewlet = self.viewlet(self.portal)
        self.assertFalse(viewlet.enabled())

    def test_metadata_viewlet_is_enabled_on_portal_with_full_view(self):
        self.portal.setLayout('folder_full_view')
        viewlet = self.viewlet(self.portal)
        self.assertTrue(viewlet.enabled())

    def test_metadata_viewlet_is_enabled_on_content(self):
        viewlet = self.viewlet(self.obj)
        self.assertTrue(viewlet.enabled())

    # FIXME: we need to rethink this feature
    @unittest.skipIf(IS_PLONE_5, 'Plone 5 includes metadata by default')
    def test_metadata_viewlet_is_disabled_on_content_edit(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', self.obj.absolute_url() + '/edit')
        try:
            html = self.obj.atct_edit()  # Archetypes
        except AttributeError:
            html = self.obj.restrictedTraverse('@@edit')()  # Dexterity
        self.assertNotIn('og:site_name', html)

    def test_metadata_viewlet_rendering(self):
        viewlet = self.viewlet(self.obj)
        html = viewlet.render()
        self.assertIn('og:title', html)
        self.assertIn('og:description', html)
        self.assertIn('og:type', html)
        self.assertIn('og:url', html)
        self.assertIn('og:image', html)
        self.assertIn('og:image:width', html)
        self.assertIn('og:image:height', html)
        self.assertIn('og:image:type', html)
        self.assertIn('og:locale', html)
        self.assertIn('og:site_name', html)

    @unittest.skipIf(skip_profiling, 'Skipping performance measure and code profiling')
    def test_metadata_viewlet_rendering_performance(self):
        self._enable_all_plugins()
        times, limit = 1000, 5  # rendering 1000 times must take less than 5ms
        viewlet = self.viewlet(self.obj)

        @timecall(immediate=True)
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render(times)

        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, limit)

        # show rendering profile
        @profile
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        render(times)


class LikeViewletTestCase(ViewletBaseTestCase):

    def setUp(self):
        super(LikeViewletTestCase, self).setUp()
        with api.env.adopt_roles(['Manager']):
            api.content.transition(obj=self.obj, transition='publish')

    def viewlet(self, context):
        return self._get_viewlet_by_name('sc.social.likes', context)

    def test_social_viewlet_is_disabled_on_portal(self):
        viewlet = self.viewlet(self.portal)
        self.assertFalse(viewlet.enabled())

    def test_social_viewlet_is_enabled_on_content(self):
        viewlet = self.viewlet(self.obj)
        self.assertTrue(viewlet.enabled())

    def test_social_viewlet_is_disabled_on_content_edit(self):
        request = self.layer['request']
        request.set('ACTUAL_URL', self.obj.absolute_url() + '/edit')
        try:
            html = self.obj.atct_edit()  # Archetypes
        except AttributeError:
            html = self.obj.restrictedTraverse('@@edit')()  # Dexterity
        self.assertNotIn('id="viewlet-social-like"', html)

    def test_social_viewlet_rendering(self):
        viewlet = self.viewlet(self.obj)
        html = viewlet.render()
        self.assertIn('id="viewlet-social-like"', html)
        self.assertIn('class="horizontal"', html)

    def test_rendermethod_default(self):
        viewlet = self.viewlet(self.obj)
        self.assertEqual(viewlet.render_method, 'plugin')

    def test_rendermethod_privacy(self):
        api.portal.set_registry_record(do_not_track, True)
        viewlet = self.viewlet(self.obj)
        self.assertEqual(viewlet.render_method, 'link')

    def test_rendermethod_privacy_opt_cookie(self):
        api.portal.set_registry_record(do_not_track, False)
        self.request.cookies['social-optout'] = 'true'
        viewlet = self.viewlet(self.obj)
        self.assertEqual(viewlet.render_method, 'link')

    def test_rendermethod_privacy_donottrack(self):
        api.portal.set_registry_record(do_not_track, False)
        self.request.environ['HTTP_DNT'] = '1'
        viewlet = self.viewlet(self.obj)
        self.assertEqual(viewlet.render_method, 'link')

    @unittest.skipIf(skip_profiling, 'Skipping performance measure and code profiling')
    def test_social_viewlet_rendering_performance(self):
        self._enable_all_plugins()
        times, limit = 1000, 5  # rendering 1000 times must take less than 5ms
        viewlet = self.viewlet(self.obj)

        @timecall(immediate=True)
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render(times)

        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, limit)

        # show rendering profile
        @profile
        def render(times):
            for i in xrange(0, times):
                viewlet.render()

        render(times)
