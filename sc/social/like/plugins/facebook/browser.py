# -*- coding:utf-8 -*-
from Acquisition import aq_parent, aq_inner
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
from urllib import urlencode
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
    fbshow_like = True
    fbshow_share = False

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)

        self.context = context
        self.title = context.title
        self.description = context.Description()
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = facebook_language(get_language(context), self.language)
        self.image = get_content_image(context, width=1200, height=630)
        self.fbshow_like = 'Like' in self.fbbuttons
        self.fbshow_share = 'Share' in self.fbbuttons
        self.button = self.typebutton

    def fbjs(self):
        js_source = """
    (function() {
        var po = document.createElement('script');
        po.async = true;
        po.src = document.location.protocol + '//connect.facebook.net/%s/all.js#xfbml=1';
        var head = document.getElementsByTagName('head')[0];
        head.appendChild(po);
    }());
    """ % self.language
        return js_source

    def image_height(self):
        """ Return height to image
        """
        img = self.image
        if img:
            return img.height

    def image_type(self):
        """ Return content type to image
        """
        img = self.image
        if img:
            return getattr(img, 'content_type',
                           getattr(img, 'mimetype', 'image/jpeg'))

    def image_width(self):
        """ Return width to image
        """
        img = self.image
        if img:
            return img.width

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
        typebutton = api.portal.get_registry_record('sc.social.like.typebutton')

        if typebutton == 'horizontal':
            typebutton = 'button_count'
            self.width = '90px'
        else:
            typebutton = 'box_count'
            self.width = '55px'
        return typebutton

    @property
    def fbaction(self):
        return api.portal.get_registry_record('sc.social.like.fbaction')

    @property
    def fbapp_id(self):
        return api.portal.get_registry_record('sc.social.like.fbapp_id')

    @property
    def fbadmins(self):
        return api.portal.get_registry_record('sc.social.like.fbadmins')

    @property
    def fbbuttons(self):
        return api.portal.get_registry_record('sc.social.like.fbbuttons')

    def _isPortalDefaultView(self):
        context = self.context
        if ISiteRoot.providedBy(aq_parent(aq_inner(context))):
            putils = getToolByName(context, 'plone_utils')
            return putils.isDefaultPage(context)
        return False

    def _isPortal(self):
        context = self.context
        if ISiteRoot.providedBy(aq_inner(context)):
            return True
        return self._isPortalDefaultView()

    def type(self):
        if self._isPortal():
            return 'website'
        return 'article'

    def share_link(self):
        absolute_url = self.context.absolute_url()
        params = dict(
            app_id=self.fbapp_id,
            display='popup',
            href=absolute_url,
            redirect_uri=absolute_url,
        )
        url = 'https://www.facebook.com/dialog/share?' + urlencode(params)
        return url
