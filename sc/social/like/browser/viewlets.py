# -*- coding: utf-8 -*-
from Products.CMFCore.WorkflowCore import WorkflowException  # noqa
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile  # noqa
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from zope.component import getMultiAdapter
from zope.component import getUtility


class BaseLikeViewlet(ViewletBase):

    enabled_portal_types = []
    typebutton = ''
    plugins_enabled = []
    render_method = ''

    def __init__(self, context, request, view, manager):
        super(BaseLikeViewlet, self).__init__(context, request, view, manager)
        self.context = context
        self.request = request
        self.view = view
        self.helper = getMultiAdapter((self.context, self.request),
                                      name='sl_helper')
        self.typebutton = self.helper.typebutton()

    @memoize
    def plugins(self):
        context = self.context
        render_method = self.render_method
        rendered = []
        plugins = self.helper.plugins()
        for plugin in plugins:
            if plugin and getattr(plugin, render_method)():
                view = context.restrictedTraverse(plugin.view())
                html_generator = getattr(view, render_method, None)
                if html_generator:
                    rendered.append({'id': plugin.id,
                                     'html': html_generator()})
        return rendered

    def enabled(self):
        """Check if the viewlet should be visible on this context."""
        try:
            published = api.content.get_state(self.context) == 'published'
        except WorkflowException:
            # no workflow on context, like in site root
            published = True
        return all([published, self.helper.enabled(self.view), self.plugins()])

    # HACK: fixes https://bitbucket.org/takaki/sc.social.like/issue/1
    def update(self):
        """Overriding ViewletBase because we may be called for
        UnauthorizedBinding objects
        """
        return


class SocialMetadataViewlet(BaseLikeViewlet):
    """Open Graph properties and plugin specific metadata."""

    index = ViewPageTemplateFile('templates/metadata.pt')
    render_method = 'metadata'

    def update(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISocialLikeSettings, check=False)
        self.helper = getMultiAdapter((self.context, self.request), name='sl_helper')
        # Most of the properties formerly defined here are unnecessary for
        # the template to render, since these template values are already
        # supplied by Plone 6 core.

    def render(self):
        if self.enabled():
            return self.index()
        return ''

    def enabled(self):
        """Check if the viewlet should be shown in this context."""
        template = self.helper.view_template_id()
        # If using folder_full_view or all_content, we add metadata
        # in order to proper display share buttons for
        # contained content types
        if template in ('all_content', 'folder_full_view'):
            return True
        return self.helper.enabled(self.view)


class SocialLikesViewlet(BaseLikeViewlet):
    """Viewlet used to display the buttons."""

    render = ViewPageTemplateFile('templates/sociallikes.pt')

    @property
    def render_method(self):
        # global cookie settings for privacy level
        if self.request.cookies.get('social-optout', None) == 'true' or \
                self.request.get_header('HTTP_DNT') == '1':
            return 'link'

        # site specific privacy level check
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        do_not_track = api.portal.get_registry_record(record, default=False)

        if do_not_track:
            return 'link'

        return 'plugin'
