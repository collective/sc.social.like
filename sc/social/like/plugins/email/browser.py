# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    metadata = None
    plugin = link = ViewPageTemplateFile('plugin.pt')

    @property
    def klass(self):
        klass = 'share-by-email pat-plone-modal'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        try:
            do_not_track = api.portal.get_registry_record(record)
        except InvalidParameterError:
            do_not_track = False
        if do_not_track:
            klass += ' link'
        return klass
