# -*- coding:utf-8 -*-
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.config import DEFAULT_ENABLED_CONTENT_TYPES
from sc.social.like.config import DEFAULT_PLUGINS_ENABLED
from sc.social.like.utils import validate_canonical_domain
from sc.social.like.utils import validate_like_ref
from sc.social.like.vocabularies import FacebookButtonsVocabulary
from sc.social.like.vocabularies import FacebookLikeActionVocabulary
from sc.social.like.vocabularies import FacebookLikeColorschemeVocabulary
from sc.social.like.vocabularies import FacebookLikeLayoutVocabulary
from sc.social.like.vocabularies import FacebookShareLayoutVocabulary
from sc.social.like.vocabularies import FacebookSizeVocabulary
from sc.social.like.vocabularies import TypeButtonVocabulary
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant

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
        fields=[
            'canonical_domain',
            'facebook_username',
            'facebook_app_id',
            'fbbuttons',
            'fbshare_layout',
            'fbshare_mobile_iframe',
            'fbshare_size',
            'fblike_action',
            'fblike_colorscheme',
            'fblike_kid_directed_site',
            'fblike_layout',
            'fblike_ref',
            'fblike_share',
            'fblike_show_faces',
            'fblike_size',
            'fblike_width',
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

    # variable name is the same as Plone 5
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

    # variable name is the same as Plone 5
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
        default=(u'Share', ),
    )

    fbshare_layout = schema.Choice(
        title=_(u'Share Layout'),
        description=_(
            u'help_share_layout',
            default=u'Selects one of the different layouts that '
                    u'are available for the plugin. Can be one of '
                    u'"box_count", "button_count", "button".',
        ),
        required=False,
        default=u'box_count',
        vocabulary=FacebookShareLayoutVocabulary,
    )

    fbshare_mobile_iframe = schema.Bool(
        title=_(u'Share Mobile iframe'),
        description=_(
            u'help_share_mobile_iframe',
            default=u'If set to true, the share button will open the '
                    u'share dialog in an iframe (instead of a popup) '
                    u'on top of your website on mobile. This option '
                    u'is only available for mobile, not desktop. For '
                    u'more information see Mobile Web Share Dialog.',
        ),
        required=False,
        default=True,
    )

    fbshare_size = schema.Choice(
        title=_(u'Share Size'),
        description=_(
            u'help_share_size',
            default=u'The button is offered in 2 sizes i.e. "large" '
                    u'and "small".',
        ),
        default=u'small',
        required=False,
        vocabulary=FacebookSizeVocabulary,
    )

    fblike_action = schema.Choice(
        title=_(u'Like Action'),
        description=_(
            u'help_like_action',
            default=u'The verb to display on the button. Can be '
                    u'either "like" or "recommend".',
        ),
        default=u'like',
        required=False,
        vocabulary=FacebookLikeActionVocabulary,
    )

    fblike_colorscheme = schema.Choice(
        title=_(u'Like Color Scheme'),
        description=_(
            u'help_like_colorscheme',
            default=u'The color scheme used by the plugin for '
                    u'any text outside of the button itself. '
                    u'Can be "light" or "dark".',
        ),
        default=u'light',
        required=False,
        vocabulary=FacebookLikeColorschemeVocabulary,
    )

    fblike_kid_directed_site = schema.Bool(
        title=_(u'Like Kid Directed Site'),
        description=_(
            u'help_like_kid_directed_site',
            default=u'If your web site or online service, or a '
                    u'portion of your service, is directed to '
                    u'children under 13 you must enable this.',
        ),
        required=False,
        default=True,
    )

    fblike_layout = schema.Choice(
        title=_(u'Like Layout'),
        description=_(
            u'help_like_layout',
            default=u'Selects one of the different layouts that '
                    u'are available for the plugin. Can be one of '
                    u'"standard", "button_count", "button" or '
                    u'"box_count".',
        ),
        default=u'button_count',
        required=False,
        vocabulary=FacebookLikeLayoutVocabulary,
    )

    fblike_ref = schema.ASCIILine(
        title=_(u'Like Tracking Referrals'),
        description=_(
            u'help_like_ref',
            default=u'A label for tracking referrals which must '
                    u'be less than 50 characters and can contain '
                    u'alphanumeric characters and some '
                    u'punctuation (currently "+/=-.:_").',
        ),
        constraint=validate_like_ref,
        required=False,
        default='',
    )

    fblike_share = schema.Bool(
        title=_(u'Like Share'),
        description=_(
            u'help_like_share',
            default=u'Specifies whether to include a share '
                    u'button beside the Like button.',
        ),
        required=False,
        default=False,
    )

    fblike_show_faces = schema.Bool(
        title=_(u'Like Show Faces'),
        description=_(
            u'help_like_show_faces',
            default=u'Specifies whether to display profile photos '
                    u'below the button (standard layout only). You '
                    u'must not enable this on child-directed sites.'
        ),
        required=False,
        default=False,
    )

    fblike_size = schema.Choice(
        title=_(u'Like Size'),
        description=_(
            u'help_like_size',
            default=u'The button is offered in 2 sizes i.e. "large" '
                    u'and "small".',
        ),
        required=False,
        default=u'small',
        vocabulary=FacebookSizeVocabulary,
    )

    fblike_width = schema.Int(
        title=_(u'Like Width'),
        description=_(
            u'help_like_width',
            default=u'The width of the plugin (standard layout only), '
                    u'which is subject to the minimum and default width.'
        ),
        required=False,
        default=90,
    )

    @invariant
    def validate_like_width(data):
        if u'Like' not in data.fbbuttons:
            return
        layout_min_width = {
            u'standard': 225,
            u'box_count': 55,
            u'button_count': 90,
            u'button': 47
        }
        min_width = layout_min_width[data.fblike_layout]
        if data.fblike_width < min_width:
            raise Invalid(_(u'For layout "{layout}" the min width is "{width}"'.format(
                layout=data.fblike_layout, width=min_width)))

    model.fieldset(
        'twitter', label=u'Twitter', fields=['twitter_username'])

    # variable name is the same as Plone 5
    twitter_username = schema.ASCIILine(
        title=_(u'Twitter nick'),
        description=_(
            u'help_your_twitter_nick',
            default=u'Enter your twitter nick. eg. simplesconsultoria',
        ),
        required=False,
        default='',
    )
