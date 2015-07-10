# -*- coding:utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from plone.memoize.view import memoize


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
        """Validates if the viewlet should be enabled for this context
        """
        return self.helper.enabled() and self.plugins()

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
        tools = getMultiAdapter((self.context, self.request),
                                name=u'plone_tools')
        site_properties = tools.properties()
        # global cookie settings for privacy level
        if self.request.cookies.get('social-optout', None) == 'true' or \
                self.request.get_header('HTTP_DNT') == '1':
            return 'link'
        # site specific privacy level check
        if getattr(site_properties, 'sc_social_likes_properties', None) \
                and getattr(site_properties.sc_social_likes_properties,
                            'do_not_track', None) and \
                site_properties.sc_social_likes_properties.do_not_track:
            return 'link'
        return 'plugin'
