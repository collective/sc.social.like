# -*- coding:utf-8 -*-
from plone import api
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

    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()
        self.portal_title = portal_state.portal_title()
        self.url = self.context.absolute_url()
        self.image = get_content_image(self.context, scale='large')
        self.language = get_language(self.context)

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
        if not self.image:
            return self.site_url + '/logo.png'
        return self.image.url

    @property
    def typebutton(self):
        record = dict(
            name='typebutton', interface=ISocialLikeSettings, default='')
        if api.portal.get_registry_record(**record) == 'horizontal':
            return 'beside'
        return 'above'

    def share_link(self):
        # See http://stackoverflow.com/questions/10690019/link-to-pin-it-on-pinterest-without-generating-a-button
        params = dict(
            url=self.context.absolute_url(),
            media=self.image_url(),
            description=self.context.Title(),
        )
        return 'http://pinterest.com/pin/create/button?' + urlencode(params)
