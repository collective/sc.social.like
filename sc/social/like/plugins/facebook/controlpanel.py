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
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

verbs = SimpleVocabulary([
    SimpleTerm(value=u'like', title=_(u'Like')),
    SimpleTerm(value=u'recommend', title=_(u'Recommend')),
])


class IFacebookSchema(Interface):
    """ Facebook configurations """

    fbaction = schema.Choice(
        title=_(u'Verb to display'),
        description=_(
            u'help_verb_display',
            default=u"The verb to display in the facebook button. "
                    u"Currently only 'like' and 'recommend' are "
                    u"supported.",
        ),
        required=True,
        default=u'like',
        vocabulary=verbs,
    )

    fbadmins = schema.TextLine(
        title=_(u'Admins'),
        description=_(
            u'help_admins',
            default=u"A comma-separated list of either the "
                    u"Facebook IDs of page administrators.",
        ),
        required=False,
    )

    fbapp_id = schema.TextLine(
        title=_(u'Application ID'),
        description=_(
            u'help_appid',
            default=u"A Facebook Platform application ID.",
        ),
        required=False,
    )


class ControlPanelAdapter(BaseControlPanelAdapter):
    """ Facebook control panel adapter """
    adapts(IPloneSiteRoot)
    implements(IFacebookSchema)

    fbaction = PFP(IFacebookSchema['fbaction'])
    fbadmins = PFP(IFacebookSchema['fbadmins'])
    fbapp_id = PFP(IFacebookSchema['fbapp_id'])


class ProviderControlPanel(ControlPanelForm):
    """ """
    form_fields = FormFields(IFacebookSchema)

    label = _('Social: Facebook settings')
    description = _('Configure settings for Facebook integration.')
