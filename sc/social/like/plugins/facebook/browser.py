# -*- coding:utf-8 -*-
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.facebook.utils import facebook_language
from zope.component import getMultiAdapter

BASE_URL = 'https://www.facebook.com/plugins/like.php?'
PARAMS = 'locale=%s&href=%s&send=false&layout=%s&show_faces=true&action=%s'


class PluginView(BrowserView):

    enabled_portal_types = []
    typebutton = ''
    fb_enabled = False
    fbaction = ''
    fbadmins = ''
    language = 'en_US'

    metadata = ViewPageTemplateFile("templates/metadata.pt")
    plugin = ViewPageTemplateFile("templates/plugin.pt")

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.title = context.title
        self.description = context.description
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
        if self.sheet:
            self.fbaction = self.sheet.getProperty("fbaction", "")
            self.fbadmins = self.sheet.getProperty("fbadmins", "")
            self.button = self.typebutton

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
        else:
            # Let's assume image as a valid fieldname
            field = 'image'
        try:
            view = context.unrestrictedTraverse('@@images')
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
            typebutton = 'button_count'
            self.width = '90px'
        else:
            typebutton = 'box_count'
            self.width = '55px'
        return typebutton
