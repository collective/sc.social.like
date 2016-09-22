# -*- coding: utf-8 -*-
"""A tile that embeds a Facebook Page.

For additional implementation detail see:
https://developers.facebook.com/docs/plugins/page-plugin
"""
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone import api
# from plone.autoform import directives as form
from plone.memoize import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like import LikeMessageFactory as _
from sc.social.like.interfaces import ISocialLikeSettings
from urllib import urlencode
# from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


TabsOptions = SimpleVocabulary([
    SimpleTerm(value='timeline', title=_(u'Timeline')),
    SimpleTerm(value='events', title=_(u'Events')),
    SimpleTerm(value='messages', title=_(u'Messages')),
])


class IFacebookTile(IPersistentCoverTile):

    """A tile that embeds a Facebook Page."""

    href = schema.URI(
        title=_(u'Facebook Page'),
        description=_(u'The URL of the Facebook Page.'),
        required=True,
    )

    width = schema.Int(
        title=_(u'Width'),
        description=_(
            u'Set the maximum width of the widget between 180 and 500 pixels. '
            u'Leave it empty to automatically adjust the widget to the width of the tile.'
        ),
        required=False,
        default=None,
        min=180,
        max=500,
    )

    height = schema.Int(
        title=_(u'Height'),
        description=_(
            u'Set the height of a displayed widget, overriding the value stored with the widget ID. '
            u'Must be greater than 70 pixels. '
        ),
        required=True,
        default=500,
        min=70,
    )

    # form.widget('tabs', CheckBoxFieldWidget)
    # tabs = schema.Choice(
    #     title=_(u'Tabs to render'),
    #     required=False,
    #     default='timeline',
    #     vocabulary=TabsOptions,
    # )

    hide_cover = schema.Bool(
        title=_(u'Hide cover photo in the header'),
        default=True,
    )

    show_facepile = schema.Bool(
        title=_(u'Show profile photos when friends like this'),
        default=False,
    )

    hide_cta = schema.Bool(
        title=_(u'Hide the custom call to action button (if available)'),
        default=True,
    )

    small_header = schema.Bool(
        title=_(u'Show small header'),
        default=True,
    )


@implementer(IFacebookTile)
class FacebookTile(PersistentCoverTile):

    """A tile that embeds a Facebook Page."""

    index = ViewPageTemplateFile('facebook.pt')
    is_configurable = False
    is_droppable = False
    is_editable = True

    @property
    @view.memoize
    def appId(self):
        appId = api.portal.get_registry_record(
            'facebook_app_id', interface=ISocialLikeSettings)
        return appId

    @property
    def is_empty(self):
        return not self.appId

    def accepted_ct(self):
        return []

    @property
    def width(self, default=500):
        if self.data['width']:
            return self.data['width']
        return default

    @property
    def height(self, default=500):
        if self.data['height']:
            return self.data['height']
        return default

    @property
    def tabs(self):
        """TODO: Return a comma-separated string of tabs to render."""
        return 'timeline'

    def _bool2str(self, field, default):
        if self.data[field]:
            return str(self.data[field]).lower()
        return default

    @property
    def adapt_container_width(self):
        if self.data['width']:
            return 'false'
        return 'true'

    @property
    def get_data(self):
        data = dict(
            adapt_container_width=self.adapt_container_width,
            height=self.height,
            hide_cover=self._bool2str('hide_cover', 'false'),
            hide_cta=self._bool2str('hide_cta', 'false'),
            href=self.data.get('href', ''),
            show_facepile=self._bool2str('show_facepile', 'true'),
            small_header=self._bool2str('small_header', 'false'),
            tabs=self.tabs,
        )
        if self.width:
            data['width'] = self.width

        return urlencode(data) + '&' + self.appId
