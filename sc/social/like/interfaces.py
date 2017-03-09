# -*- coding:utf-8 -*-
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.config import DEFAULT_ENABLED_CONTENT_TYPES
from sc.social.like.config import DEFAULT_PLUGINS_ENABLED
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
        'facebook',
        label=u'Facebook',
        fields=['fbaction', 'facebook_username', 'facebook_app_id', 'fbbuttons', 'fbshowlikes'],
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
