# -*- coding:utf-8 -*-
"""Helper view to generate Facebook widget.

More information:
* https://developers.facebook.com/docs/plugins
"""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_language
from urllib import urlencode


class PluginView(BrowserView):
    """Helper view to generate Facebook widget."""

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

    def portal_url(self):
        portal = api.portal.get()
        return portal.absolute_url()

    def canonical_url(self):
        if ISocialMedia.providedBy(self.context):
            return self.context.canonical_url
        return self.context.absolute_url()

    def is_plone_5(self):
        return IS_PLONE_5

    def fbjs(self):
        language = facebook_language(get_language(self.context), 'en_US')
        return """
    (function() {{
        var po = document.createElement('script');
        po.async = true;
        po.src = document.location.protocol + '//connect.facebook.net/{0}/all.js#xfbml=1';
        var head = document.getElementsByTagName('head')[0];
        head.appendChild(po);
    }}());
    """.format(language)

    def typebutton(self):
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        typebutton = api.portal.get_registry_record(record, default='')
        record = ISocialLikeSettings.__identifier__ + '.fbshowlikes'
        fbshowlikes = api.portal.get_registry_record(record, default=True)
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

    def fbaction(self):
        record = ISocialLikeSettings.__identifier__ + '.fbaction'
        return api.portal.get_registry_record(record, default='')

    def app_id(self):
        record = ISocialLikeSettings.__identifier__ + '.facebook_app_id'
        return api.portal.get_registry_record(record, default='')

    def admins(self):
        record = ISocialLikeSettings.__identifier__ + '.facebook_username'
        return api.portal.get_registry_record(record, default='')

    def fbshow_like(self):
        record = ISocialLikeSettings.__identifier__ + '.fbbuttons'
        fbbuttons = api.portal.get_registry_record(record, default=[])
        return 'Like' in fbbuttons

    def fbshow_share(self):
        record = ISocialLikeSettings.__identifier__ + '.fbbuttons'
        fbbuttons = api.portal.get_registry_record(record, default=[])
        return 'Share' in fbbuttons

    def share_link(self):
        params = {
            'app_id': self.app_id(),
            'display': 'popup',
            'href': self.canonical_url(),
            'redirect_uri': self.context.absolute_url(),
        }
        return 'https://www.facebook.com/dialog/share?' + urlencode(params)
