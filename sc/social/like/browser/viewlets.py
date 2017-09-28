# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.formwidget.namedfile.converter import b64decode_file
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
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
    """Open Graph properties and plugin specific metadata."""

    index = ViewPageTemplateFile('templates/metadata.pt')
    render_method = 'metadata'

    def update(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISocialLikeSettings, check=False)
        self.helper = getMultiAdapter((self.context, self.request), name=u'sl_helper')
        self.title = self.context.Title()
        self.description = self.context.Description()
        portal = api.portal.get()
        self.site_name = portal.Title()
        self.language = facebook_language(get_language(self.context), 'en_US')
        self.image = get_content_image(self.context)

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
        if template in ('all_content', 'folder_full_view',):
            return True
        return self.helper.enabled(self.view)

    def portal_url(self):
        portal = api.portal.get()
        return portal.absolute_url()

    def canonical_url(self):
        if ISocialMedia.providedBy(self.context):
            return self.context.canonical_url
        return self.context.absolute_url()

    def get_fallback_image(self):
        fallback_image = self.settings.fallback_image
        if fallback_image is not None:
            filename, _ = b64decode_file(fallback_image)
            return '/@@sociallike-fallback-image/' + filename
        else:
            return '/logo.png'

    def image_url(self):
        """Return lead image URL."""
        img = self.image
        if img:
            return img.url
        else:
            return self.portal_url() + self.get_fallback_image()

    def image_width(self):
        return self.image.width

    def image_height(self):
        return self.image.height

    def image_type(self):
        """Return lead image MIME type."""
        try:
            return self.image.content_type  # Dexterity
        except AttributeError:
            return self.image.mimetype  # Archetypes

    def type(self):
        context = aq_inner(self.context)
        context_state = api.content.get_view(
            'plone_context_state', context, self.request)
        if context_state.is_portal_root():
            return 'website'
        return 'article'


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
