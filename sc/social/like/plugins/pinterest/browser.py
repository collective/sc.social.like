# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


BASE_URL = '//pinterest.com/pin/create/button/'
PARAMS = '?url={0}&media={1}&description={2}'


class PluginView(BrowserView):

    pinterest_enabled = False
    language = 'en'

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # FIXME: the following could rise unexpected exceptions
        #        move it to a new setup() method
        #        see: http://docs.plone.org/develop/plone/views/browserviews.html#creating-a-view
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.image = get_content_image(context, scale='large')
        self.language = get_language(context)

    def share_url(self):
        template = BASE_URL + PARAMS
        return template.format(
            self.url,
            self.image_url(),
            self.context.Title(),
        )

    def image_url(self):
        """ Return url to image
        """
        img = self.image
        if img:
            return img.url
        else:
            return '{0}/logo.png'.format(self.site_url)

    @property
    def typebutton(self):
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        try:
            typebutton = api.portal.get_registry_record(record)
        except InvalidParameterError:
            typebutton = ''

        if typebutton == 'horizontal':
            typebutton = 'beside'
        else:
            typebutton = 'above'
        return typebutton

    def share_link(self):
        # See http://stackoverflow.com/questions/10690019/link-to-pin-it-on-pinterest-without-generating-a-button
        params = dict(
            url=self.context.absolute_url(),
            media=self.image_url(),
            description=self.context.Title(),
        )
        url = 'http://pinterest.com/pin/create/button?' + urlencode(params)
        return url
