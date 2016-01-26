# -*- coding:utf-8 -*-
from sc.social.like.plugins import IPlugin
from sc.social.like.plugins import Plugin
from zope.interface import implements
from controlpanel import IFacebookControlPanel  # flake8: noqa


class Facebook(Plugin):
    implements(IPlugin)

    id = 'facebook'
    name = 'Facebook'
