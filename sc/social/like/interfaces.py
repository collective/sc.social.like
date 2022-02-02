# -*- coding:utf-8 -*-
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.config import DEFAULT_ENABLED_CONTENT_TYPES
from sc.social.like.config import DEFAULT_PLUGINS_ENABLED
from sc.social.like.utils import validate_og_fallback_image
from sc.social.like.vocabularies import FacebookButtonsVocabulary
from sc.social.like.vocabularies import FacebookVerbsVocabulary
from sc.social.like.vocabularies import TypeButtonVocabulary
from zope import schema
from zope.interface import Interface

import sys


# BBB: for compatibility with installations made before 2.5.0
sys.modules['sc.social.like.interfaces.socialikes'] = sys.modules[__name__]


class ISocialLikeLayer(Interface):

    """A layer specific for this add-on product."""


class ISocialLikes(Interface):
    """
    """


class IHelperView(Interface):

    """Social Like configuration helpers."""

    def configs():
        """Social Like configuration."""

    def enabled_portal_types():
        """Portal Types that will display our viewlet."""

    def plugins_enabled():
        """List of plugins enabled."""

    def typebutton():
        """Button to be used."""

    def enabled(view):
        """Validates if the viewlet should be enabled for this context."""

    def available_plugins():
        """Return available plugins."""

    def plugins():
        """Return enabled plugins."""

    def view_template_id():
        """View or template id for this context."""


class ISocialLikeSettings(model.Schema):
    """Schema for the control panel form."""

    enabled_portal_types = schema.Tuple(
        title=_('Content types'),
        description=_(
            'help_portal_types',
            default='Please select content types in which the '
                    'viewlet will be applied.',
        ),
        required=True,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'),
    )

    plugins_enabled = schema.Tuple(
        title=_('Plugins'),
        description=_(
            'help_enabled_plugins',
            default='Please select which plugins will be used',
        ),
        required=False,
        default=DEFAULT_PLUGINS_ENABLED,
        value_type=schema.Choice(vocabulary='sc.social.likes.plugins'),
    )

    folderish_templates = schema.List(
        title=_('Folderish Templates'),
        description=_(
            'help_folderish_templates',
            default='If a folderish has one of these templates as default '
                    'view, the viewlet is showed even if the folderish type '
                    'is not selected in Content types.',
        ),
        required=False,
        value_type=schema.TextLine(),
    )

    validation_enabled = schema.Bool(
        title=_('Enable content validation?'),
        description=_(
            'help_validation_enabled',
            default='Enables validation to check if content follows social networks sharing best practices. '
                    'The validation includes title, description and lead image fields. '
                    'This feature is only available for Dexterity-based content types.'),
        default=True,
    )

    typebutton = schema.Choice(
        title=_('Button style'),
        description=_(
            'help_selected_buttons',
            default='Choose your button style.',
        ),
        required=True,
        default='horizontal',
        vocabulary=TypeButtonVocabulary,
    )

    do_not_track = schema.Bool(
        title=_('Do not track users'),
        description=_(
            'help_do_not_track',
            default='If enabled, the site will not provide advanced sharing '
                    'widgets; simple links will be used instead.\n'
                    'This will limit user experience and features '
                    u"(like the share count) but will enhance users' privacy: "
                    'no 3rd party cookies will be sent to users.'),
        default=False,
    )

    model.fieldset(
        'open_graph',
        label='Open Graph',
        fields=[
            'fallback_image',
        ],
    )

    # The former property canonical_domain is now removed since Plone 6 core
    # already generates and serves a canonical URL for every page.

    form.widget('fallback_image', NamedImageFieldWidget)
    fallback_image = schema.Bytes(
        title=_('Fallback image'),
        description=_(
            'help_fallback_image',
            default='Content without a lead image will use this image as fallback (<code>og:image</code> property). '
                    'There could be a delay of up to 2 minutes when replacing this image.'),
        required=False,
        constraint=validate_og_fallback_image,
    )

    model.fieldset(
        'facebook',
        label='Facebook',
        fields=[
            'fbaction',
            'facebook_username',
            'facebook_app_id',
            'fbbuttons',
            'fbshowlikes',
            'facebook_prefetch_enabled',
        ],
    )

    fbaction = schema.Choice(
        title=_('Verb to display'),
        description=_(
            'help_verb_display',
            default='The verb to display in the Facebook button. '
                    'Currently only "like" and "recommend" are '
                    'supported.'),
        required=True,
        default='like',
        vocabulary=FacebookVerbsVocabulary,
    )

    facebook_username = schema.ASCIILine(
        title=_('Admins'),
        description=_(
            'help_admins',
            default='A comma-separated list of either the '
                    'Facebook IDs of page administrators.'),
        required=False,
        default='',
    )

    facebook_app_id = schema.ASCIILine(
        title=_('Application ID'),
        description=_(
            'help_appid',
            default='A Facebook Platform application ID.\n'
                    'This is required when the \"Do not track users\" option is enabled and for the '
                    'Facebook share icon to be displayed. See https://developers.facebook.com/docs/apps#register'),
        required=False,
        default='',
    )

    fbbuttons = schema.Tuple(
        title=_('Facebook buttons'),
        description=_(
            'help_fbbuttons',
            default='Select buttons to be shown',
        ),
        value_type=schema.Choice(vocabulary=FacebookButtonsVocabulary),
        required=True,
        default=('Like',),
    )

    fbshowlikes = schema.Bool(
        title=_('Show number of likes'),
        description=_(
            'help_show_likes',
            default='If enabled, the Facebook button will show the number of '
                    'Facebook users who have already liked this page.'),
        default=True,
    )

    facebook_prefetch_enabled = schema.Bool(
        title=_('Enable Facebook prefetch?'),
        description=_(
            'help_facebook_prefetch_enabled',
            default='If enabled, an event is triggered to make Facebook '
                    'crawler scrape and cache metadata every time a new '
                    'piece content is published and every time published '
                    'content is edited. '
                    'This will keep the metadata updated on Facebook always.'),
        default=False,
    )

    model.fieldset(
        'twitter', label='Twitter', fields=['twitter_username'])

    twitter_username = schema.ASCIILine(
        title=_('Twitter nick'),
        description=_(
            'help_your_twitter_nick',
            default='Enter your twitter nick. eg. simplesconsultoria'),
        required=False,
        default='',
    )
