# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implementer


@implementer(IPlugin)
class Pinterest(Plugin):

    id = 'pinterest'
    name = 'Pinterest'

    def config_view(self):
        # No configuration view
        return None

    def metadata(self):
        return None
