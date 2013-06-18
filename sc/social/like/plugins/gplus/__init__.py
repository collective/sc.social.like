# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements


class GooglePlus(Plugin):
    implements(IPlugin)

    id = 'gplus'
    name = 'Google+'

    def config_view(self):
        # No configuration view
        return None
