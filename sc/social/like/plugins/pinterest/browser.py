# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter

BASE_URL = '//pinterest.com/pin/create/button/'
PARAMS = '?url=%s&media=%s&description=%s'


class PluginView(BrowserView):

    typebutton = ''
    pinterest_enabled = False
    language = 'en'

    metadata = ViewPageTemplateFile("templates/metadata.pt")
    plugin = ViewPageTemplateFile("templates/plugin.pt")

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.image = get_content_image(context, scale='large')
        self.language = get_language(context)
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)

    def share_url(self):
        template = BASE_URL + PARAMS
        return template % (
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
            return '%s/logo.png' % self.site_url

    @property
    def typebutton(self):
        typebutton = self.sheet.getProperty("typebutton", "")
        if typebutton == 'horizontal':
            typebutton = 'beside'
        else:
            typebutton = 'above'
        return typebutton
