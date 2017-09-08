# -*- coding: utf-8 -*-
from plone import api
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
from zope import schema
from zope.component import getUtility

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

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(self.portal, 'News Item', 'test-1')
            self.obj.setTitle('Etiam pulvinar rutrum diam vitae malesuada')
            self.obj.setDescription(u'Aenean maximus eu eros in congue. '
                                    u'Etiam maximus congue purus quis pellentesque.')
            set_image_field(self.obj, load_image(1024, 768), 'image/png')
            self.obj.reindexObject()

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

    def test_validate_social_content_publish_valid(self):

        request = self.obj.REQUEST

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')

        messages = IStatusMessage(request).show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, u'Item state changed.')
        self.assertEqual(messages[0].type, u'info')

    # def test_validate_social_content_edit_valid(self):
    #
    #     with api.env.adopt_roles(['Manager']):
    #         self.obj.setTitle('Phasellus tempus sagittis vulputate')
    #
    #     messages = IStatusMessage(self.request).show()
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(messages[0].message, u'Item state changed.')
    #     self.assertEqual(messages[0].type, u'info')

    # def test_validate_social_content_publish_title_invalid(self):
    #
    #     self.obj.setTitle('Duis vestibulum arcu eu risus viverra semper. Donec scelerisque '
    #                       'venenatis libero, quis pellentesque dui fringilla eget.')
    #
    #     api.content.transition(self.obj, 'publish')
    #
    #     messages = IStatusMessage(self.request).show()
    #     self.assertEqual(len(messages), 2)
    #     self.assertEqual(messages[1].message, u'Title have more than 70 characters.')
    #     self.assertEqual(messages[1].type, u'warning')
    #
    # def test_validate_social_content_publish_description_invalid(self):
    #
    #     self.obj.setDescription('Duis vestibulum arcu eu risus viverra semper. Donec scelerisque '
    #                             'venenatis libero, quis pellentesque dui fringilla eget.')
    #
    #     api.content.transition(self.obj, 'publish')
    #
    #     messages = IStatusMessage(self.request).show()
    #     self.assertEqual(len(messages), 2)
    #     self.assertEqual(messages[1].message, u'Title have more than 70 characters.')
    #     self.assertEqual(messages[1].type, u'warning')
    #
    # def test_validate_social_content_publish_image_dimension_invalid(self):
    #
    #     set_image_field(self.obj, load_image(200, 200), 'image/png')
    #
    #     api.content.transition(self.obj, 'publish')
    #
    #     messages = IStatusMessage(self.request).show()
    #     self.assertEqual(len(messages), 2)
    #     self.assertEqual(messages[1].message, u'Title have more than 70 characters.')
    #     self.assertEqual(messages[1].type, u'warning')
