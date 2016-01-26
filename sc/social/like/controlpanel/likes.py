# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from datetime import date
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from Products.CMFPlone.utils import getToolByName
from sc.social.like import LikeMessageFactory as _
from sc.social.like.plugins import IPlugin
from zope import schema
from zope.component import getUtilitiesFor
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


CONTENT_TYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'

styles = SimpleVocabulary([
    SimpleTerm(value=u'horizontal', title=_(u'horizontal')),
    SimpleTerm(value=u'vertical', title=_(u'vertical')),
])


def default_enabled_portal_types():
    return ('Document', 'Event', 'News Item')


class ISocialLikeControlPanel(Interface):

    enabled_portal_types = schema.Tuple(
        title=_(u'Content types'),
        description=_(
            u'help_portal_types',
            default=u'Please select content types in which the '
                    u'viewlet will be applied.',
        ),
        required=True,
        defaultFactory=default_enabled_portal_types,
        value_type=schema.Choice(vocabulary=CONTENT_TYPES)
    )

    plugins_enabled = schema.Tuple(
        title=_(u'Plugins'),
        description=_(
            u'help_enabled_plugins',
            default=u'Please select which plugins will be used',
        ),
        required=False,
        value_type=schema.Choice(vocabulary='sc.social.likes.plugins')
    )

    typebutton = schema.Choice(
        title=_(u'Button style'),
        description=_(
            u'help_selected_buttons',
            default=u'Choose your button style.',
        ),
        required=True,
        default=_(u'horizontal'),
        vocabulary=styles,
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


class SocialLikeControlPanelForm(RegistryEditForm):
    schema = ISocialLikeControlPanel
    schema_prefix = "sc.social.like"
    label = u'Social Like Settings'

    def plugins_configs(self):
        """ Return Plugins and their configuration pages """
        context = aq_inner(self.context)
        portal_url = getToolByName(context, 'portal_url')()
        registered = dict(getUtilitiesFor(IPlugin))
        plugins = []
        for name in registered:
            plugin = registered[name]
            config_view = plugin.config_view()
            if config_view:
                url = '%s/%s' % (portal_url, config_view)
                plugins.append({'name': name,
                                'url': url})
        return plugins


SocialLikeControlPanelView = layout.wrap_form(
    SocialLikeControlPanelForm, ControlPanelFormWrapper)
