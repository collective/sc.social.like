# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements


class WhatsApp(Plugin):
    implements(IPlugin)

    id = 'whatsapp'
    name = 'WhatsApp'

    def config_view(self):
        # No configuration view
        return None
