# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.api.exc import InvalidParameterError
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


BASE_URL = 'https://www.facebook.com/plugins/like.php?'
PARAMS = 'locale={0}&href={1}&send=false&layout={2}&show_faces=true&action={3}'


class PluginView(BrowserView):

    fb_enabled = False
    language = 'en_US'

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # FIXME: the following could rise unexpected exceptions
        #        move it to a new setup() method
        #        see: http://docs.plone.org/develop/plone/views/browserviews.html#creating-a-view
        self.title = context.title
        self.description = context.Description()
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = facebook_language(get_language(context), self.language)
        self.image = get_content_image(context, width=1200, height=630)
        self.typebutton  # XXX: needed to initialize self.width

    @property
    def is_plone_5(self):
        return IS_PLONE_5

    def fbjs(self):
        js_source = """
    (function() {{
        var po = document.createElement('script');
        po.async = true;
        po.src = document.location.protocol + '//connect.facebook.net/{0}/all.js#xfbml=1';
        var head = document.getElementsByTagName('head')[0];
        head.appendChild(po);
    }}());
    """.format(self.language)
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
            return '{0}/logo.png'.format(self.site_url)

    @property
    def typebutton(self):
        typerecord = ISocialLikeSettings.__identifier__ + '.typebutton'
        showlikesrecord = ISocialLikeSettings.__identifier__ + '.fbshowlikes'

        try:
            typebutton = api.portal.get_registry_record(typerecord)
            fbshowlikes = api.portal.get_registry_record(showlikesrecord)
        except InvalidParameterError:
            typebutton = ''
            fbshowlikes = True
        if typebutton == 'horizontal' and fbshowlikes:
            typebutton = 'button_count'
            self.width = '90px'
        elif typebutton == 'vertical' and fbshowlikes:
            typebutton = 'box_count'
            self.width = '55px'
        else:
            # no counts, show simple button
            typebutton = 'button'
            self.width = '55px'

        return typebutton

    @property
    def fbaction(self):
        record = ISocialLikeSettings.__identifier__ + '.fbaction'
        try:
            return api.portal.get_registry_record(record)
        except InvalidParameterError:
            return ''

    @property
    def app_id(self):
        record = ISocialLikeSettings.__identifier__ + '.facebook_app_id'
        try:
            return api.portal.get_registry_record(record)
        except InvalidParameterError:
            return ''

    @property
    def admins(self):
        record = ISocialLikeSettings.__identifier__ + '.facebook_username'
        try:
            return api.portal.get_registry_record(record)
        except InvalidParameterError:
            return ''

    @property
    def fbshow_like(self):
        record = ISocialLikeSettings.__identifier__ + '.fbbuttons'
        try:
            return 'Like' in api.portal.get_registry_record(record)
        except InvalidParameterError:
            return False

    @property
    def fbshow_share(self):
        record = ISocialLikeSettings.__identifier__ + '.fbbuttons'
        try:
            return 'Share' in api.portal.get_registry_record(record)
        except InvalidParameterError:
            return False

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
            app_id=self.app_id,
            display='popup',
            href=absolute_url,
            redirect_uri=absolute_url,
        )
        url = 'https://www.facebook.com/dialog/share?' + urlencode(params)
        return url
