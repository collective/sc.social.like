# -*- coding:utf-8 -*-

from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFDefault.formlib.schema import ProxyFieldProperty as PFP
from Products.CMFPlone.interfaces import IPloneSiteRoot
from sc.social.like import LikeMessageFactory as _
from sc.social.like.controlpanel.likes import BaseControlPanelAdapter
from zope import schema
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.interface import Interface


class ITwitterSchema(Interface):
    """ Twitter configurations """

    twittvia = schema.TextLine(
        title=_(u'Twitter nick'),
        description=_(
            u'help_your_twitter_nick',
            default=u"Enter your twitter nick. eg. simplesconsultoria",
        ),
        required=False,
    )


class ControlPanelAdapter(BaseControlPanelAdapter):
    """ Twitter control panel adapter """
    adapts(IPloneSiteRoot)
    implements(ITwitterSchema)

    twittvia = PFP(ITwitterSchema['twittvia'])


class ProviderControlPanel(ControlPanelForm):
    """ """
    form_fields = FormFields(ITwitterSchema)

    label = _('Social: Twitter settings')
    description = _('Configure settings for Twitter integration.')
