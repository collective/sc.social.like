# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from plone.app.layout.globals.interfaces import IViewView
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from sc.social.like.interfaces import IHelperView
from sc.social.like.plugins import IPlugin
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class HelperView(BrowserView):
    """ Social Like configuration helpers
    """
    implements(IHelperView)

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
    def enabled_portal_types(self):
        registry = getUtility(IRegistry)
        return registry.get('sc.social.like.enabled_portal_types')

    @memoize_contextless
    def plugins_enabled(self):
        registry = getUtility(IRegistry)
        return registry.get('sc.social.like.plugins_enabled')

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
        enabled = self.plugins_enabled() or ()
        plugins = []
        for plugin_id in enabled:
            plugin = available.get(plugin_id, None)
            if plugin:
                plugins.append(plugin)
        return plugins

    @memoize_contextless
    def typebutton(self):
        registry = getUtility(IRegistry)
        return registry.get('sc.social.like.typebutton')

    @memoize_contextless
    def do_not_track(self):
        registry = getUtility(IRegistry)
        return registry.get('sc.social.like.do_not_track')

    @memoize
    def view_template_id(self):
        return self.context_state.view_template_id()
