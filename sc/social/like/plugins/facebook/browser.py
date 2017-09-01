# -*- coding:utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


BASE_URL = 'https://www.facebook.com/plugins/like.php?'
PARAMS = 'locale={0}&href={1}&send=false&layout={2}&show_faces=true&action={3}'


class PluginView(BrowserView):

    fb_enabled = False
    language = 'en_US'

    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        self.title = self.context.title
        self.description = self.context.Description()
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()
        self.url = self.context.absolute_url()
        self.language = facebook_language(get_language(self.context), self.language)
        self.typebutton  # XXX: needed to initialize self.width

    @property
    def canonical_url(self):
        if not ISocialMedia.providedBy(self.context):
            # use current URL if the object don't provide the behavior
            return self.url
        return self.context.canonical_url

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

    @property
    def typebutton(self):
        record = dict(
            name='typebutton', interface=ISocialLikeSettings, default=None)
        typebutton = api.portal.get_registry_record(**record)
        record = dict(
            name='fbshowlikes', interface=ISocialLikeSettings, default=None)
        fbshowlikes = api.portal.get_registry_record(**record)
        if None in (typebutton, fbshowlikes):
            typebutton = ''
            fbshowlikes = True
        if typebutton == 'horizontal' and fbshowlikes:
            self.width = '90px'
            return 'button_count'
        elif typebutton == 'vertical' and fbshowlikes:
            self.width = '55px'
            return 'box_count'
        # no counts, show simple button
        self.width = '55px'
        return 'button'

    @property
    def fbaction(self):
        record = dict(
            name='fbaction', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    @property
    def app_id(self):
        record = dict(
            name='facebook_app_id', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    @property
    def admins(self):
        record = dict(
            name='facebook_username', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    @property
    def fbshow_like(self):
        record = dict(
            name='fbbuttons', interface=ISocialLikeSettings, default=False)
        return 'Like' in api.portal.get_registry_record(**record)

    @property
    def fbshow_share(self):
        record = dict(
            name='fbbuttons', interface=ISocialLikeSettings, default=False)
        return 'Share' in api.portal.get_registry_record(**record)

    def share_link(self):
        params = dict(
            app_id=self.app_id,
            display='popup',
            href=self.canonical_url,
            redirect_uri=self.url,
        )
        return 'https://www.facebook.com/dialog/share?' + urlencode(params)
