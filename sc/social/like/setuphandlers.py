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
            'sc.social.like:uninstall',
            'sc.social.like.upgrades.v2000:default',
            'sc.social.like.upgrades.v3000:default',
            'sc.social.like.upgrades.v3010:default',
            'sc.social.like.upgrades.v3020:default',
        ]
