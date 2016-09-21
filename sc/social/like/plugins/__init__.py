# -*- coding:utf-8 -*-
from sc.social.like.plugins.interfaces import IPlugin  # noqa


class Plugin(object):
    """ Social Like Plugin Base Class"""

    id = ''
    name = ''

    def config_view(self):
        return '@@{0}-config'.format(self.id)

    def view(self):
        return '@@{0}-plugin'.format(self.id)

    def metadata(self):
        return 'metadata'

    def plugin(self):
        return 'plugin'

    def link(self):
        return 'link'
