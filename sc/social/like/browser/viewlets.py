# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
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
    language = 'en_US'

    render = ViewPageTemplateFile('templates/metadata.pt')

    def __init__(self, context, request, view, manager):
        super(SocialMetadataViewlet, self).__init__(context, request, view, manager)
        self.setup()

    def setup(self):
        self.title = self.context.title
        self.description = self.context.Description()
        portal = api.portal.get()
        self.site_url = portal.absolute_url()
        self.url = self.context.absolute_url()
        self.language = facebook_language(get_language(self.context), self.language)
        self.image = get_content_image(self.context)

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

    @property
    def via(self):
        record = dict(
            name='twitter_username', interface=ISocialLikeSettings, default='')
        return api.portal.get_registry_record(**record)

    @property
    def canonical_url(self):
        if not ISocialMedia.providedBy(self.context):
            # use current URL if the object don't provide the behavior
            return self.url
        return self.context.canonical_url

    def image_height(self):
        """ Return height to image
        """
        if not self.image:
            return
        return self.image.height

    def image_type(self):
        """ Return content type to image
        """
        if not self.image:
            return
        type = getattr(self.image, 'content_type', None)
        if type is not None:
            return type
        return getattr(self.image, 'mimetype', 'image/jpeg')

    def image_width(self):
        """ Return width to image
        """
        if not self.image:
            return
        return self.image.width

    def image_url(self):
        """ Return url to image
        """
        if not self.image:
            return self.site_url + '/logo.png'
        return self.image.url

    def _isPortalDefaultView(self):
        if not ISiteRoot.providedBy(aq_parent(aq_inner(self.context))):
            return False
        putils = api.portal.get_tool('plone_utils')
        return putils.isDefaultPage(self.context)

    def _isPortal(self):
        if ISiteRoot.providedBy(aq_inner(self.context)):
            return True
        return self._isPortalDefaultView()

    def type(self):
        if self._isPortal():
            return 'website'
        return 'article'


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
