# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implementer


@implementer(IPlugin)
class Email(Plugin):

    id = 'email'
    name = 'Email'

    def config_view(self):
        return None  # no configuration view
