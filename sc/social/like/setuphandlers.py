# -*- coding:utf-8 -*-
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone import interfaces as plone_interfaces
from zope.interface import implements


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return ['sc.social.like.upgrades.v2000',
                'sc.social.like.upgrades.v3000',
                'sc.social.like.upgrades.v3010',
                'sc.social.like.upgrades.v3020',
                ]


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'sc.social.like:uninstall',
            u'sc.social.like.upgrades.v2000:default',
            u'sc.social.like.upgrades.v3000:default',
            u'sc.social.like.upgrades.v3010:default',
            u'sc.social.like.upgrades.v3020:default',
        ]
