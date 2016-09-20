# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.globals.interfaces import IViewView
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from sc.social.like.interfaces import IHelperView
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins import IPlugin
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.interface import implementer


@implementer(IHelperView)
class HelperView(BrowserView):
    """ Social Like configuration helpers
    """

    def __init__(self, context, request, *args, **kwargs):
        super(HelperView, self).__init__(context, request, *args, **kwargs)
        context = aq_inner(context)
        self.context = context
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')

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
    def plugins_enabled(self):
        configs = self.configs()
        return configs.plugins_enabled or []

    @memoize
    def enabled(self, view=None):
        if view and not IViewView.providedBy(view):
            return False
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
        return self.context_state.view_template_id()
