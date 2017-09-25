# -*- coding: utf-8 -*-
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage
from sc.social.like.interfaces import ISocialLikeSettings


class FallBackImage(Download):
    """Helper view to return the fallback image."""

    def __init__(self, context, request):
        super(FallBackImage, self).__init__(context, request)

        record = ISocialLikeSettings.__identifier__ + '.fallback_image'
        fallback_image = api.portal.get_registry_record(record, default=None)

        if fallback_image is not None:
            # set fallback image data for download
            filename, data = b64decode_file(fallback_image)
            data = NamedImage(data=data, filename=filename)
            self.filename, self.data = filename, data
            # enable image caching for 2 minutes
            self.request.RESPONSE.setHeader('Cache-Control', 'max-age=120, public')
        else:
            # resource no longer available
            self.data = NamedImage(data='')
            self.request.RESPONSE.setStatus(410)  # Gone

    def _getFile(self):
        return self.data
