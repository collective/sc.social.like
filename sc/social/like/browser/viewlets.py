# -*- coding:utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins import IPlugin
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor


class BaseLikeViewlet(ViewletBase):

    enabled_portal_types = []
    typebutton = ''
    plugins_enabled = []
    render_method = ''

    def __init__(self, context, request, view, manager):
        super(BaseLikeViewlet, self).__init__(context, request, view, manager)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        self.site_url = self.portal_state.portal_url()
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        self.enabled_portal_types = self.sheet.getProperty(
            'enabled_portal_types',
            []
        )
        self.plugins_enabled = self.sheet.getProperty('plugins_enabled',
                                                      [])

    def available_plugins(self):
        registered = dict(getUtilitiesFor(IPlugin))
        return registered

    def _plugins(self):
        available = self.available_plugins()
        enabled = self.plugins_enabled
        plugins = []
        for plugin_id in enabled:
            plugin = available.get(plugin_id, None)
            if plugin:
                plugins.append(plugin)
        return plugins

    def plugins(self):
        context = self.context
        render_method = self.render_method
        rendered = []
        plugins = self._plugins()
        for plugin in plugins:
            if plugin and render_method:
                view = context.restrictedTraverse(plugin.view())
                html = getattr(view, render_method)()
                rendered.append({'id': plugin.id,
                                 'html': html})
        return rendered

    def enabled(self):
        """Validates if the viewlet should be enabled for this context
        """
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types

    # HACK: fixes https://bitbucket.org/takaki/sc.social.like/issue/1
    def update(self):
        """Overriding ViewletBase because we may be called for
        UnauthorizedBinding objects
        """
        return


class SocialMetadataViewlet(BaseLikeViewlet):
    """Viewlet used to insert metadata into page header
    """
    render = ViewPageTemplateFile("templates/metadata.pt")
    render_method = 'metadata'


class SocialLikesViewlet(BaseLikeViewlet):
    """Viewlet used to display the buttons
    """
    render = ViewPageTemplateFile("templates/sociallikes.pt")
    render_method = 'plugin'
