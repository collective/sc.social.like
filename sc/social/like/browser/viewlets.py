# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from zope.component import getMultiAdapter


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
                                      name=u'sl_helper')
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
        return all([published, self.helper.enabled(), self.plugins()])

    # HACK: fixes https://bitbucket.org/takaki/sc.social.like/issue/1
    def update(self):
        """Overriding ViewletBase because we may be called for
        UnauthorizedBinding objects
        """
        return


class SocialMetadataViewlet(BaseLikeViewlet):
    """Viewlet used to insert metadata into page header
    """
    render = ViewPageTemplateFile('templates/metadata.pt')
    render_method = 'metadata'

    def enabled(self):
        """Validates if the viewlet should be enabled for this context
        """
        template = self.helper.view_template_id()
        # If using folder_full_view or all_content, we add metadata
        # in order to proper display share buttons for
        # contained content types
        if template in ('all_content', 'folder_full_view',):
            return True
        return self.helper.enabled(self.view)


class SocialLikesViewlet(BaseLikeViewlet):
    """Viewlet used to display the buttons
    """
    render = ViewPageTemplateFile('templates/sociallikes.pt')

    @property
    def render_method(self):
        # global cookie settings for privacy level
        if self.request.cookies.get('social-optout', None) == 'true' or \
                self.request.get_header('HTTP_DNT') == '1':
            return 'link'

        # site specific privacy level check
        record = ISocialLikeSettings.__identifier__ + '.do_not_track'
        try:
            do_not_track = api.portal.get_registry_record(record)
        except InvalidParameterError:
            do_not_track = False

        if do_not_track:
            return 'link'

        return 'plugin'
