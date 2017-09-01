# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    plugin = link = ViewPageTemplateFile('plugin.pt')

    @property
    def klass(self):
        klass = 'share-by-email pat-plone-modal'
        record = dict(
            name='do_not_track', interface=ISocialLikeSettings, default=False)
        if api.portal.get_registry_record(**record):
            return klass + ' link'
        return klass
