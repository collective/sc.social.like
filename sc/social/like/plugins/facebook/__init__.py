# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements


class Facebook(Plugin):
    implements(IPlugin)

    id = 'facebook'
    name = 'Facebook'
