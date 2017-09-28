# -*- coding:utf-8 -*-
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.config import DEFAULT_ENABLED_CONTENT_TYPES
from sc.social.like.config import DEFAULT_PLUGINS_ENABLED
from sc.social.like.utils import validate_canonical_domain
from sc.social.like.utils import validate_og_fallback_image
from sc.social.like.vocabularies import FacebookButtonsVocabulary
from sc.social.like.vocabularies import FacebookVerbsVocabulary
from sc.social.like.vocabularies import TypeButtonVocabulary
from zope import schema
from zope.interface import Interface

# BBB: for compatibility with installations made before 2.5.0
import sys


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
        title=_(u'Content types'),
        description=_(
            u'help_portal_types',
            default=u'Please select content types in which the '
                    u'viewlet will be applied.',
        ),
        required=True,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes')
    )

    plugins_enabled = schema.Tuple(
        title=_(u'Plugins'),
        description=_(
            u'help_enabled_plugins',
            default=u'Please select which plugins will be used',
        ),
        required=False,
        default=DEFAULT_PLUGINS_ENABLED,
        value_type=schema.Choice(vocabulary='sc.social.likes.plugins')
    )

    validation_enabled = schema.Bool(
        title=_(u'Enable content validation?'),
        description=_(
            u'help_validation_enabled',
            default=u'Enables validation to check if content follows social networks sharing best practices. '
                    u'The validation includes title, description and lead image fields. '
                    u'This feature is only available for Dexterity-based content types.'
        ),
        default=True,
    )

    typebutton = schema.Choice(
        title=_(u'Button style'),
        description=_(
            u'help_selected_buttons',
            default=u'Choose your button style.',
        ),
        required=True,
        default=u'horizontal',
        vocabulary=TypeButtonVocabulary,
    )

    do_not_track = schema.Bool(
        title=_(u'Do not track users'),
        description=_(
            u'help_do_not_track',
            default=u'If enabled, the site will not provide advanced sharing '
                    u'widgets , instead simple links will be used.\n'
                    u'This will limits user experience and features '
                    u'(like the share count) but will enhance users privacy: '
                    u'no 3rd party cookies will be sent to users.'
        ),
        default=False,
    )

    model.fieldset(
        'open_graph',
        label=u'Open Graph',
        fields=[
            'canonical_domain',
            'fallback_image',
        ],
    )

    canonical_domain = schema.URI(
        title=_(u'Canonical domain'),
        description=_(
            u'help_canonical_domain',
            default=u'The canonical domain will be used to construct the canonical URL (<code>og:url</code> property) of portal objects. '
                    u'Use the domain name of your site (e.g. <strong>http://www.example.org</strong> or <strong>https://www.example.org</strong>). '
                    u'Facebook will use the canonical URL to ensure that all actions such as likes and shares aggregate at the same URL rather than spreading across multiple versions of a page. '
                    u'Check <a href="https://pypi.python.org/pypi/sc.social.like">package documentation</a> for more information on how to use this feature.'
        ),
        required=True,
        constraint=validate_canonical_domain,
    )

    form.widget('fallback_image', NamedImageFieldWidget)
    fallback_image = schema.ASCII(
        title=_(u'Fallback image'),
        description=_(
            u'help_fallback_image',
            default=u'Content without a lead image will use this image as fallback (<code>og:image</code> property). '
                    u'There could be a delay of up to 2 minutes when replacing this image.'
        ),
        required=False,
        constraint=validate_og_fallback_image,
    )

    model.fieldset(
        'facebook',
        label=u'Facebook',
        fields=[
            'fbaction',
            'facebook_username',
            'facebook_app_id',
            'fbbuttons',
            'fbshowlikes',
            'facebook_prefetch_enabled'
        ],
    )

    fbaction = schema.Choice(
        title=_(u'Verb to display'),
        description=_(
            u'help_verb_display',
            default=u'The verb to display in the Facebook button. '
                    u'Currently only "like" and "recommend" are '
                    u'supported.',
        ),
        required=True,
        default=u'like',
        vocabulary=FacebookVerbsVocabulary,
    )

    facebook_username = schema.ASCIILine(
        title=_(u'Admins'),
        description=_(
            u'help_admins',
            default=u'A comma-separated list of either the '
                    u'Facebook IDs of page administrators.',
        ),
        required=False,
        default='',
    )

    facebook_app_id = schema.ASCIILine(
        title=_(u'Application ID'),
        description=_(
            u'help_appid',
            default=u'A Facebook Platform application ID.\n'
                    u'This is required when \"Do not track users\" option is enabled.',
        ),
        required=False,
        default='',
    )

    fbbuttons = schema.Tuple(
        title=_(u'Facebook buttons'),
        description=_(
            u'help_fbbuttons',
            default=u'Select buttons to be shown',
        ),
        value_type=schema.Choice(vocabulary=FacebookButtonsVocabulary),
        required=True,
        default=(u'Like', ),
    )

    fbshowlikes = schema.Bool(
        title=_(u'Show number of likes'),
        description=_(
            u'help_show_likes',
            default=u'If enabled, the Facebook button will show the number of '
                    u'Facebook users who have already liked this page.'
        ),
        default=True,
    )

    facebook_prefetch_enabled = schema.Bool(
        title=_(u'Enable Facebook prefetch?'),
        description=_(
            u'help_facebook_prefetch_enabled',
            default=u'If enabled, an event is triggered to make Facebook '
                    u'crawler scrape and cache metadata every time a new '
                    u'piece content is published and every time published '
                    u'content is edited. '
                    u'This will keep the metadata updated on Facebook always.'
        ),
        default=False,
    )

    model.fieldset(
        'twitter', label=u'Twitter', fields=['twitter_username'])

    twitter_username = schema.ASCIILine(
        title=_(u'Twitter nick'),
        description=_(
            u'help_your_twitter_nick',
            default=u'Enter your twitter nick. eg. simplesconsultoria',
        ),
        required=False,
        default='',
    )
