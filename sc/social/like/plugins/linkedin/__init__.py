# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements


class LinkedIn(Plugin):
    implements(IPlugin)

    id = 'linkedin'
    name = 'LinkedIn'

    def config_view(self):
        # No configuration view
        return None
