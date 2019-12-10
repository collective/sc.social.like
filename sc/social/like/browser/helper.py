# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.layout.globals.interfaces import IViewView
from plone.formwidget.namedfile.converter import b64decode_file
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IFolderish
from Products.Five import BrowserView
from sc.social.like.interfaces import IHelperView
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins import IPlugin
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import implementer


@implementer(IHelperView)
class HelperView(BrowserView):
    """Social Like configuration helpers."""

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

    @memoize_contextless
    def configs(self):
        registry = getUtility(IRegistry)
        # do not fail if the upgrade step has not being run
        settings = registry.forInterface(ISocialLikeSettings, check=False)
        return settings

    @memoize_contextless
    def enabled_portal_types(self):
        configs = self.configs()
        return configs.enabled_portal_types or []

    @memoize_contextless
    def folderish_templates(self):
        configs = self.configs()
        return configs.folderish_templates or []

    @memoize_contextless
    def plugins_enabled(self):
        configs = self.configs()
        return configs.plugins_enabled or []

    @memoize
    def enabled(self, view):
        if view and not IViewView.providedBy(view):
            return False
        if view and IFolderContentsView.providedBy(view):
            return False
        folderish_templates = self.folderish_templates()
        template = self.view_template_id()
        if IFolderish.providedBy(self.context) and \
                template in folderish_templates:
            return True
        enabled_portal_types = self.enabled_portal_types()
        return self.context.portal_type in enabled_portal_types

    @memoize_contextless
    def available_plugins(self):
        registered = dict(getUtilitiesFor(IPlugin))
        return registered

    @memoize_contextless
    def plugins(self):
        available = self.available_plugins()
        enabled = self.plugins_enabled()
        plugins = []
        for plugin_id in enabled:
            plugin = available.get(plugin_id, None)
            if plugin:
                plugins.append(plugin)
        return plugins

    @memoize_contextless
    def typebutton(self):
        configs = self.configs()
        return configs.typebutton

    @memoize
    def view_template_id(self):
        context_state = api.content.get_view(
            'plone_context_state', self.context, self.request)
        return context_state.view_template_id()


class FallBackImageView(Download):
    """Helper view to return the fallback image."""

    def __init__(self, context, request):
        super(FallBackImageView, self).__init__(context, request)

        record = ISocialLikeSettings.__identifier__ + '.fallback_image'
        fallback_image = api.portal.get_registry_record(record, default=None)

        if fallback_image is not None:
            # set fallback image data for download
            filename, data = b64decode_file(fallback_image)
            data = NamedImage(data=data, filename=filename)
            self.filename, self.data = filename, data
            # enable image caching for 2 minutes
            self.request.RESPONSE.setHeader('Cache-Control', 'max-age=120, public')
        else:
            # resource no longer available
            self.data = NamedImage(data='')
            self.request.RESPONSE.setStatus(410)  # Gone

    def _getFile(self):
        return self.data
