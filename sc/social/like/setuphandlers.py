# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone import interfaces as plone_interfaces
from zope.interface import implements


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return ['sc.social.like.upgrades.v2000',
                'sc.social.like.upgrades.v3000']


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'sc.social.like:uninstall',
            u'sc.social.like.upgrades.v2000:default',
            u'sc.social.like.upgrades.v3000:default',
        ]


def install(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('sc.social.like_install.txt') is None:
        return

    # Add additional setup code here


def uninstall(context):

    if context.readDataFile('sc.social.like_uninstall.txt') is None:
        return

    portal = context.getSite()
    portal_conf = getToolByName(portal, 'portal_controlpanel')
    portal_conf.unregisterConfiglet('@@likes-providers')

    # Remove tweetmeme_properties in portal properties
    pp = getToolByName('portal_properties')

    try:
        if hasattr(pp, 'sc_social_likes_properties'):
            pp.manage_delObjects(ids='sc_social_likes_properties')
    except KeyError:
        pass
