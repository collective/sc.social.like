# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter

from plone.app.testing import logout

from Products.CMFCore.utils import getToolByName

from sc.social.like.testing import INTEGRATION_TESTING


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST), name='likes-providers')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_protected(self):
        # control panel view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse, '@@likes-providers')

    def test_configlet_install(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        installed = [a.getAction(self)['id'] for a in controlpanel.listActions()]
        self.failUnless('sociallikes' in installed)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
