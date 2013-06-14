# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements


class Twitter(Plugin):
    implements(IPlugin)

    id = 'twitter'
    name = 'Twitter'
