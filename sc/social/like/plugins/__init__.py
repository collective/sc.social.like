# -*- coding:utf-8 -*-
from sc.social.like.plugins.interfaces import IPlugin  # noqa


class Plugin(object):
    ''' Social Like Plugin Base Class'''

    id = ''
    name = ''

    def config_view(self):
        return '@@%s-config' % self.id

    def view(self):
        return '@@%s-plugin' % self.id

    def metadata(self):
        return 'metadata'

    def plugin(self):
        return 'plugin'
