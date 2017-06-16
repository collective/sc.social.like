# -*- coding: utf-8 -*-
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from plone.supermodel import model
from sc.social.like.config import IS_PLONE_5
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import INTEGRATION_TESTING
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
