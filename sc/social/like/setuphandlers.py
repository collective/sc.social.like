# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        return [
            'sc.social.like.upgrades.v2000',
            'sc.social.like.upgrades.v3000',
            'sc.social.like.upgrades.v3010',
            'sc.social.like.upgrades.v3020',
        ]


@implementer(plone_interfaces.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [
            u'sc.social.like:uninstall',
            u'sc.social.like.upgrades.v2000:default',
            u'sc.social.like.upgrades.v3000:default',
            u'sc.social.like.upgrades.v3010:default',
            u'sc.social.like.upgrades.v3020:default',
        ]
