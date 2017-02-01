# -*- coding: utf-8 -*-
"""A tile that embeds a Twitter timeline.

For additional implementation detail see:
https://dev.twitter.com/web/embedded-timelines/parameters
"""
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
# from plone.autoform import directives as form
from plone.memoize import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like import LikeMessageFactory as _
from sc.social.like.interfaces import ISocialLikeSettings
# from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


ChromeOptions = SimpleVocabulary([
    SimpleTerm(value='noheader', title=_(u'Hide the timeline header')),
    SimpleTerm(value='nofooter', title=_(u'Hide the timeline footer')),
    SimpleTerm(value='noborders', title=_(u'Remove all borders within the widget')),
    SimpleTerm(value='noscrollbar', title=_(u'Crop and hides the main timeline scrollbar')),
    SimpleTerm(value='transparent', title=_(u"Remove the widget's background color")),
])


class ITwitterTile(IPersistentCoverTile):

    """A tile that embeds a Twitter timeline."""

    widget_id = schema.ASCIILine(
        title=_(u'Widget ID'),
        required=False,
        default='',
    )

    width = schema.Int(
        title=_(u'Width'),
        description=_(
            u'Set the maximum width of the widget between 180 and 520 pixels. '
            u'Leave it empty to automatically adjust the widget to the width of the tile.'
        ),
        required=False,
        default=None,
        min=180,
        max=520,
    )

    height = schema.Int(
        title=_(u'Height'),
        description=_(
            u'Set the height of a displayed widget, overriding the value stored with the widget ID. '
            u'Must be greater than 200 pixels. '
            u'Note: this parameter does not apply if a tweet limit has been specified.'
        ),
        required=False,
        default=500,
        min=200,
    )

    # form.widget('chrome', CheckBoxFieldWidget)
    # chrome = schema.Choice(
    #     title=_(u'Chrome'),
    #     required=False,
    #     vocabulary=ChromeOptions,
    # )

    tweet_limit = schema.Int(
        title=_(u'Tweet limit'),
        description=_(
            u'Display an expanded timeline of between 1 and 20 tweets. '
            u'Leave it empty to use the default or to set the height of the widget.'
        ),
        required=False,
        default=None,
        min=1,
        max=20,
    )

    aria_polite = schema.Choice(
        title=_(u'WAI-ARIA politeness'),
        description=_(
            u'A timeline widget is a live region of a page which may receive updates as new tweets become available. '
            u'When specified as polite, assistive technologies will notify users of updates but generally do not interrupt the current task, and updates take low priority. '
            u'When specified as assertive, assistive technologies will immediately notify the user, and could potentially clear the speech queue of previous updates.'
        ),
        required=True,
        values=['polite', 'assertive'],
        default='polite',
    )


@implementer(ITwitterTile)
class TwitterTile(PersistentCoverTile):

    """A tile that embeds a Twitter timeline."""

    index = ViewPageTemplateFile('twitter.pt')
    is_configurable = False
    is_droppable = False
    is_editable = True

    @property
    @view.memoize
    def username(self):
        username = api.portal.get_registry_record(
            'twitter_username', interface=ISocialLikeSettings)
        if username and username.startswith('@'):
            username = username[1:]
        return username

    @property
    def is_empty(self):
        return not self.username

    def accepted_ct(self):
        return []

    @property
    def chrome(self):
        """TODO: Return a string to be used as data-chrome attribute."""
        return ''

    @property
    def aria_polite(self):
        """Return 'assertive' if it was selected."""
        aria_polite = self.data.get('aria_polite', 'polite')
        if aria_polite == 'polite':
            # using a None value on TAL attributes directives in the
            # template will remove the attribute itself; we don't want
            # to add a 'data-aria-polite' attribute if we're using
            # its default value
            return
        return aria_polite

    @property
    def get_data(self):
        return dict(
            aria_polite=self.aria_polite,
            chrome=self.chrome,
            height=self.data.get('height', 500),
            tweet_limit=self.data.get('tweet_limit', None),
            widget_id=self.data.get('widget_id', None),
            width=self.data.get('width', None),
        )
