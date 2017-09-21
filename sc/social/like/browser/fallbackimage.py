# -*- coding: utf-8 -*-
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage
from sc.social.like.interfaces import ISocialLikeSettings


class FallBackImage(Download):
    """Download fallback image file, via /@@sociallike-fallback-image/filename"""

    filename = None
    data = None

    def __call__(self):
        self.setup()
        super(FallBackImage, self).__call__()

    def setup(self):
        fallback_image = api.portal.get_registry_record('fallback_image', interface=ISocialLikeSettings, default=False)
        if fallback_image:
            filename, data = b64decode_file(fallback_image)
            data = NamedImage(data=data, filename=filename)
            self.data = data
            self.filename = filename

    def _getFile(self):
        return self.data
