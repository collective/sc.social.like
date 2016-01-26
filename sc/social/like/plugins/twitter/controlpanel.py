# -*- coding:utf-8 -*-
from sc.social.like import LikeMessageFactory as _
from zope import schema
from zope.interface import Interface
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout


class ITwitterControlPanel(Interface):
    """ Twitter configurations """

    twittvia = schema.TextLine(
        title=_(u'Twitter nick'),
        description=_(
            u'help_your_twitter_nick',
            default=u'Enter your twitter nick. eg. simplesconsultoria',
        ),
        required=False,
    )


class TwitterControlPanelForm(RegistryEditForm):
    """ """
    schema = ITwitterControlPanel
    schema_prefix = "sc.social.like"
    label = _('Social: Twitter settings')

    description = _('Configure settings for Twitter integration.')


TwitterControlPanelView = layout.wrap_form(
    TwitterControlPanelForm, ControlPanelFormWrapper)
