# -*- coding:utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from sc.social.like import LikeMessageFactory as _
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


verbs = SimpleVocabulary([
    SimpleTerm(value=u'like', title=_(u'Like')),
    SimpleTerm(value=u'recommend', title=_(u'Recommend')),
])

buttons = SimpleVocabulary([
    SimpleTerm(value=u'Like', title=_(u'Like')),
    SimpleTerm(value=u'Share', title=_(u'Share')),
])


class IFacebookControlPanel(Interface):
    """ Facebook configurations """

    fbaction = schema.Choice(
        title=_(u'Verb to display'),
        description=_(
            u'help_verb_display',
            default=u'The verb to display in the facebook button. '
                    u'Currently only "like" and "recommend" are '
                    u'supported.',
        ),
        required=True,
        default=u'like',
        vocabulary=verbs,
    )

    fbadmins = schema.TextLine(
        title=_(u'Admins'),
        description=_(
            u'help_admins',
            default=u'A comma-separated list of either the '
                    u'Facebook IDs of page administrators.',
        ),
        required=False,
    )

    fbapp_id = schema.TextLine(
        title=_(u'Application ID'),
        description=_(
            u'help_appid',
            default=u'A Facebook Platform application ID.\n'
                    u'This is required when \"Do not track users\" option is enabled.',
        ),
        required=False,
    )

    fbbuttons = schema.Tuple(
        title=_(u'Facebook buttons'),
        description=_(
            u'help_fbbuttons',
            default=u'Select buttons to be shown',
        ),
        value_type=schema.Choice(vocabulary=buttons),
        default=(u'Like', ),
        required=True,
    )


class FacebookControlPanelForm(RegistryEditForm):
    """ """
    schema = IFacebookControlPanel
    schema_prefix = "sc.social.like"
    label = _('Social: Facebook settings')

    description = _('Configure settings for Facebook integration.')


FacebookControlPanelView = layout.wrap_form(
    FacebookControlPanelForm, ControlPanelFormWrapper)
