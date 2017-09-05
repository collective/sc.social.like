# -*- coding:utf-8 -*-
"""Helper view to generate WhatsApp widget."""
from Acquisition import aq_inner
from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language


class PluginView(BrowserView):
    """Helper view to generate WhatsApp widget."""

    metadata = None
    plugin = link = ViewPageTemplateFile('templates/plugin.pt')

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.language = get_language(context)
        data = url_quote(u'{0} - {1}'.format(
            safe_unicode(self.context.title), self.context.absolute_url()))
        self.whatsappurl = u'whatsapp://send?text={0}'.format(data)

    @property
    def klass(self):
        klass = 'whatsapp'
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        do_not_track = api.portal.get_registry_record(record, default=False)
        if do_not_track:
            klass += ' link'
        return klass
