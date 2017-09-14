# -*- coding: utf-8 -*-
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from zope.component import getUtility


class ImageFallBack(Download):

    def __init__(self, context, request):
        super(ImageFallBack, self).__init__(context, request)
        self.filename = None
        self.data = None

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialLikeSettings)
        if getattr(settings, 'image_fallback', False):
            filename, data = b64decode_file(settings.image_fallback)
            data = NamedImage(data=data, filename=filename)
            self.data = data
            self.filename = filename

    def _getFile(self):
        return self.data
