# -*- coding:utf-8 -*-
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.pinterest import controlpanel
from sc.social.like.utils import facebook_language
from zope.component import getMultiAdapter

BASE_URL = '//pinterest.com/pin/create/button/'
PARAMS = '?url=%s&media=%s&description=%s'


class PluginView(BrowserView):

    typebutton = ''
    pinterest_enabled = False
    language = 'en_US'

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
        languages = self.request.get('HTTP_ACCEPT_LANGUAGE',
                                     '').split(';')[0].split(',')
        self.language = facebook_language(languages, self.language)
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)

    @property
    def prefs(self):
        portal = self.portal
        return controlpanel.IPinterestSchema(portal)

    def share_url(self):
        template = BASE_URL + PARAMS
        return template % (
            self.url,
            self.image_url(),
            self.context.Title(),
        )

    def image_url(self, scale='large'):
        """ Return url to image
        """
        fields = ['image', 'leadImage', 'portrait']
        context = self.context
        if IBaseContent.providedBy(context):
            schema = context.Schema()
            field = [field for field in schema.keys() if field in fields]
            if field:
                field = field[0]
        view = context.unrestrictedTraverse('@@images')
        try:
            img = view.scale(fieldname=field, scale=scale)
        except AttributeError:
            img = None
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
