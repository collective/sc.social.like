# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    typebutton = ''
    language = 'en'

    metadata = ViewPageTemplateFile('templates/metadata.pt')
    plugin = link = ViewPageTemplateFile('templates/plugin.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # FIXME: the following could rise unexpected exceptions
        #        move it to a new setup() method
        #        see: http://docs.plone.org/develop/plone/views/browserviews.html#creating-a-view
        self.portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = get_language(context)
        data = url_quote(u'{0} - {1}'.format(
            safe_unicode(self.context.title), self.context.absolute_url()))
        self.whatsappurl = u'whatsapp://send?text={0}'.format(data)

    @property
    def klass(self):
        klass = 'whatsapp'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        try:
            do_not_track = api.portal.get_registry_record(record)
        except InvalidParameterError:
            do_not_track = False
        if do_not_track:
            klass += ' link'
        return klass
