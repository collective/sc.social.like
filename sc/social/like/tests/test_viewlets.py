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
                self.portal,
                type='News Item',
                title='Lorem Ipsum',
                description='Neque Porro',
            )
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
        def get_meta_content(name):
            """Return the content attribute of the meta tag specified by name."""
            node = html.find('*/meta[@name="{0}"]'.format(name))
            if node is None:
                node = html.find('*/meta[@property="{0}"]'.format(name))
            return node.attrib['content']

        record = ISocialLikeSettings.__identifier__ + '.twitter_username'
        api.portal.set_registry_record(record, 'plone')
        record = ISocialLikeSettings.__identifier__ + '.facebook_username'
        api.portal.set_registry_record(record, 'plone')
        record = ISocialLikeSettings.__identifier__ + '.facebook_app_id'
        api.portal.set_registry_record(record, 'myid')

        viewlet = self.viewlet(self.obj)
        html = viewlet.render()
        from lxml import etree
        html = etree.HTML(html)
        self.assertEqual(get_meta_content('og:site_name'), 'Plone site')
        expected = r'http://nohost/plone/lorem-ipsum'
        self.assertEqual(get_meta_content('og:url'), expected)
        self.assertEqual(get_meta_content('og:type'), 'article')
        self.assertEqual(get_meta_content('og:locale'), 'en_GB')
        self.assertEqual(get_meta_content('og:title'), 'Lorem Ipsum')
        self.assertEqual(get_meta_content('og:description'), 'Neque Porro')
        expected = r'http://nohost/plone/lorem-ipsum/@@images/[0-9a-f--]+.png'
        self.assertRegexpMatches(get_meta_content('og:image'), expected)
        self.assertEqual(get_meta_content('og:image:height'), '576')
        self.assertEqual(get_meta_content('og:image:width'), '768')
        self.assertEqual(get_meta_content('og:image:type'), 'image/png')
        self.assertEqual(get_meta_content('fb:admins'), 'plone')
        self.assertEqual(get_meta_content('fb:app_id'), 'myid')
        self.assertEqual(get_meta_content('twitter:card'), 'summary_large_image')
        self.assertEqual(get_meta_content('twitter:site'), '@plone')

    def test_og_type_on_content(self):
        # At document, use article type
        viewlet = self.viewlet(self.obj)
        og_type = viewlet.type()
        self.assertIn('article', og_type)

    def test_og_type_on_portal_root(self):
        # XXX: this test code doesn't seem to be quite right
        # At document, default page of portal, use website type
        self.portal.setDefaultPage(self.obj.id)
        viewlet = self.viewlet(self.portal)
        og_type = viewlet.type()
        self.assertIn('website', og_type)

    def test_metadata_viewlet_performance(self):
        """Viewlet rendering must take less than 1ms."""
        self._enable_all_plugins()
        times = 1000
        viewlet = self.viewlet(self.obj)

        @timecall(immediate=True)
        def render_metadata_viewlet(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render_metadata_viewlet(times=times)

        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, 1)

    @unittest.skipIf(skip_profiling, 'Code profiling not being executed')
    def test_show_metadata_viewlet_rendering_profile(self):
        self._enable_all_plugins()
        times = 1000
        viewlet = self.viewlet(self.obj)

        # show rendering profile
        @profile
        def render_metadata_viewlet(times):
            for i in xrange(0, times):
                viewlet.render()

        render_metadata_viewlet(times=times)


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

    def test_social_viewlet_performance(self):
        """Viewlet rendering must take less than 2ms."""
        self._enable_all_plugins()
        times = 1000
        viewlet = self.viewlet(self.obj)

        @timecall(immediate=True)
        def render_social_viewlet(times):
            for i in xrange(0, times):
                viewlet.render()

        with capture() as out:
            render_social_viewlet(times=times)

        timelapse = float(re.search('(\d+\.\d+)', out[1]).group())
        self.assertLess(timelapse, 2)

    @unittest.skipIf(skip_profiling, 'Code profiling not being executed')
    def test_show_social_viewlet_rendering_profile(self):
        self._enable_all_plugins()
        times = 1000
        viewlet = self.viewlet(self.obj)

        # show rendering profile
        @profile
        def render_social_viewlet(times):
            for i in xrange(0, times):
                viewlet.render()

        render_social_viewlet(times=times)
