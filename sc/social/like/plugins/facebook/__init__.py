# -*- coding:utf-8 -*-:

from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implementer


@implementer(IPlugin)
class Facebook(Plugin):

    id = 'facebook'
    name = 'Facebook'
