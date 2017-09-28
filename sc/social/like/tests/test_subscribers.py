# -*- coding: utf-8 -*-
"""Subscribers related test cases.

Sharing best practices validation tests run only with Dexterity-based
content types.
"""
from plone import api
from plone.dexterity.events import EditFinishedEvent
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from plone.supermodel import model
from Products.statusmessages.interfaces import IStatusMessage
from sc.social.like.config import IS_PLONE_5
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from sc.social.like.tests.utils import get_random_string
from sc.social.like.utils import MSG_INVALID_OG_DESCRIPTION
from sc.social.like.utils import MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS
from sc.social.like.utils import MSG_INVALID_OG_TITLE
from testfixtures import log_capture
from zope import schema
from zope.component import getUtility
from zope.event import notify

import logging
import requests_mock
import unittest


class IFoo(model.Schema):
    """Dummy test schema."""
    twitter_username = schema.ASCIILine(default='')


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISocialLikeSettings)

    def test_event_with_package_uninstalled(self):
        self.registry.records['foo'] = Record(field.ASCIILine(), 'foo')
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        # should not raise exceptions on changes
        self.registry['foo'] = 'bar'

    @unittest.skipIf(IS_PLONE_5, 'This test is for Plone 4 only')
    def test_modify_plone_4(self):
        # should not raise exceptions on changes
        self.settings.twitter_username = 'hvelarde'

    @unittest.skipIf(not IS_PLONE_5, 'This test is for Plone 5 only')
    def test_modify_social_like_settings(self):
        self.settings.twitter_username = 'hvelarde'
        self.assertEqual(self.registry['plone.twitter_username'], 'hvelarde')
        # changing other fields don't break anything
        self.settings.do_not_track = True

    @unittest.skipIf(not IS_PLONE_5, 'This test is for Plone 5 only')
    def test_modify_plone_settings(self):
        from zope.schema.interfaces import WrongType
        try:
            self.registry['plone.twitter_username'] = 'hvelarde'
        except WrongType:
            # in Plone 5.0 this field type was TextLine
            self.registry['plone.twitter_username'] = u'hvelarde'
        self.assertEqual(self.settings.twitter_username, 'hvelarde')
        # changing other fields don't break anything
        self.registry['plone.share_social_data'] = False

    @unittest.skipIf(not IS_PLONE_5, 'This test is for Plone 5 only')
    def test_invalid_interface(self):
        # changes to fields with names being tracked but belonging to
        # different schemas should not modify anything
        self.registry.registerInterface(IFoo)
        settings = self.registry.forInterface(IFoo)
        settings.twitter_username = 'hvelarde'
        # both records must be unchanged
        self.assertEqual(self.settings.twitter_username, '')
        self.assertEqual(self.registry['plone.twitter_username'], '')


class ValidationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.news_item = api.content.create(
                self.portal, 'News Item', title=u'Lorem ipsum')
        set_image_field(self.news_item, load_image(1024, 768), 'image/png')

    def test_do_not_validate_on_submit(self):
        # content don't follow best practices
        self.news_item.title = get_random_string(80)
        self.news_item.description = get_random_string(300)
        set_image_field(self.news_item, load_image(200, 150), 'image/png')

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'submit')

        # no feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 0)

    def test_validate_on_publish_valid(self):
        # content follows best practices
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # no feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 0)

    def test_validate_on_publish_invalid(self):
        # content don't follow best practices
        self.news_item.title = get_random_string(80)
        self.news_item.description = get_random_string(300)
        set_image_field(self.news_item, load_image(200, 150), 'image/png')

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].message, MSG_INVALID_OG_TITLE)
        self.assertEqual(messages[0].type, u'warning')
        self.assertEqual(messages[1].message, MSG_INVALID_OG_DESCRIPTION)
        self.assertEqual(messages[1].type, u'warning')
        self.assertEqual(messages[2].message, MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)
        self.assertEqual(messages[2].type, u'warning')

    def test_validate_on_no_workflow(self):
        # image and files have no associated workflow
        with api.env.adopt_roles(['Manager']):
            image = api.content.create(self.portal, 'Image', id='foo')

        # content don't follow best practices
        image.title = get_random_string(80)
        image.description = get_random_string(300)
        set_image_field(image, load_image(200, 150), 'image/png')
        notify(EditFinishedEvent(image))

        # feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(messages[0].message, MSG_INVALID_OG_TITLE)
        self.assertEqual(messages[0].type, u'warning')
        self.assertEqual(messages[1].message, MSG_INVALID_OG_DESCRIPTION)
        self.assertEqual(messages[1].type, u'warning')
        self.assertEqual(messages[2].message, MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)
        self.assertEqual(messages[2].type, u'warning')

    def test_do_not_validate_on_edit_not_public(self):
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'submit')

        # content don't follow best practices
        self.news_item.title = get_random_string(80)
        self.news_item.description = get_random_string(300)
        set_image_field(self.news_item, load_image(200, 150), 'image/png')
        notify(EditFinishedEvent(self.news_item))

        # no feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 0)

    def test_validate_on_edit_valid(self):
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # content follows best practices
        self.news_item.title = get_random_string(70)
        self.news_item.description = get_random_string(200)
        set_image_field(self.news_item, load_image(1920, 1080), 'image/png')
        notify(EditFinishedEvent(self.news_item))

        # no feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 0)

    def test_validate_on_edit_invalid(self):
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # content don't follow best practices
        self.news_item.title = get_random_string(80)
        self.news_item.description = get_random_string(300)
        set_image_field(self.news_item, load_image(200, 150), 'image/png')
        notify(EditFinishedEvent(self.news_item))

        # no feedback messages present
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].message, MSG_INVALID_OG_TITLE)
        self.assertEqual(messages[0].type, u'warning')
        self.assertEqual(messages[1].message, MSG_INVALID_OG_DESCRIPTION)
        self.assertEqual(messages[1].type, u'warning')
        self.assertEqual(messages[2].message, MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)
        self.assertEqual(messages[2].type, u'warning')

    def test_validate_with_package_uninstalled(self):
        from sc.social.like.config import PROJECTNAME
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        # should not raise exceptions on publishing
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # should not raise exceptions on editing
        notify(EditFinishedEvent(self.news_item))


class PrefetchTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        record = ISocialLikeSettings.__identifier__ + '.facebook_prefetch_enabled'
        api.portal.set_registry_record(record, True)

        with api.env.adopt_roles(['Manager']):
            self.news_item = api.content.create(
                self.portal, 'News Item', title=u'Lorem ipsum')

        url = self.news_item.absolute_url()
        self.endpoint = 'https://graph.facebook.com/?id=' + url + '&scrape=true'

    @requests_mock.mock()
    @log_capture(level=logging.INFO)
    def test_facebook_prefetch_non_public(self, m, l):
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'submit')

        # check no log entries
        l.check()

    @requests_mock.mock()
    @log_capture(level=logging.INFO)
    def test_facebook_prefetch(self, m, l):
        m.post(self.endpoint, status_code='200')

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # check log entries
        msg = 'Prefetch successful: http://nohost/plone/lorem-ipsum'
        expected = ('sc.social.like', 'INFO', msg)
        l.check(expected)

    @requests_mock.mock()
    @log_capture(level=logging.INFO)
    def test_facebook_prefetch_error(self, m, l):
        import json
        text = '{"error":{"message":"foo","type":"bar"}}'
        m.post(self.endpoint, text=text, status_code='403', reason='Forbidden')

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # check log entries
        msg = 'Prefetch error 403 (Forbidden): ' + str(json.loads(text))
        expected = ('sc.social.like', 'WARNING', msg)
        l.check(expected)

    @requests_mock.mock()
    def test_facebook_prefetch_failure(self, m):
        import requests
        m.post(self.endpoint, exc=requests.exceptions.ConnectTimeout)

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.news_item, 'publish')

        # transition should not be aborted
        self.assertEqual(api.content.get_state(self.news_item), 'published')


def load_tests(loader, tests, pattern):
    from sc.social.like.testing import HAS_DEXTERITY

    test_cases = [ControlPanelTestCase]
    if HAS_DEXTERITY:
        # load validation tests on Dexterity-based content types only
        test_cases.append(ValidationTestCase)
        test_cases.append(PrefetchTestCase)

    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
