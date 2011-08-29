# -*- coding:utf-8 -*-

from zope.schema import Bool
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema import Choice
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from plone.app.controlpanel.form import ControlPanelForm

from plone.fieldsets.fieldsets import FormFieldsets

from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget

from sc.social.like import LikeMessageFactory as _

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

verbs = SimpleVocabulary(
    [SimpleTerm(value=u'like', title=_(u'Like')),
     SimpleTerm(value=u'recommend', title=_(u'Recommend')), ]
    )


class MultiSelectWidget(BaseMultiSelectWidget):
    """ """
    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiSelectWidget, self).__init__(field,
            field.value_type.vocabulary, request)


class IProvidersSchema(Interface):
    """ General Configurations """

    enabled_portal_types = Tuple(
        title=_(u'Content types'),
        description=_(u'help_portal_types',
                      default=u"Please select content types in which the "
                              u"viewlet will be applied.",
            ),
        required=True,
        value_type=Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
        )

    typebutton = Choice(
        title=_(u'Button style'),
        description=_(u'help_selected_buttons',
                      default=u"Choose your button style.",
            ),
        required=True,
        default=_(u'horizontal'),
        values=(_(u'horizontal'), _(u'vertical')),
        )


class ITwitterSchema(Interface):
    """ Twitter configurations """

    twitter_enabled = Bool(
        title=_(u"Enable Twitter button"),
        default=True,
        required=False,
        )

    twittvia = TextLine(
        title=_(u'Twitter nick'),
        description=_(u'help_your_twitter_nick',
                      default=u"Enter your twitter nick. eg. simplesconsultoria",
            ),
        required=False,
        )


class IFbSchema(Interface):
    """ Facebook configurations """

    fb_enabled = Bool(
        title=_(u"Enable Facebook button"),
        default=True,
        required=False,
        )

    fbaction = Choice(
        title=_(u'Verb to display'),
        description=_(u'help_verb_display',
                      default=u"The verb to display in the facebook button. "
                              u"Currently only 'like' and 'recommend' are "
                              u"supported.",
            ),
        required=True,
        default=u'like',
        vocabulary=verbs,
        )

    fbadmins = TextLine(
        title=_(u'Admins'),
        description=_(u'help_admins',
                      default=u"A comma-separated list of either the "
                              u"Facebook IDs of page administrators or a "
                              u"Facebook Platform application ID.",
            ),
        required=False,
        )


class IGpSchema(Interface):
    """ Google+ configurations """

    gp_enabled = Bool(
        title=_(u"Enable Google+ action"),
        default=True,
        required=False,
        )


class BaseControlPanelAdapter(SchemaAdapterBase):
    """ Base control panel adapter """

    def __init__(self, context):
        super(BaseControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.sc_social_likes_properties


class LikeControlPanelAdapter(BaseControlPanelAdapter):
    """ Like control panel adapter """
    adapts(IPloneSiteRoot)
    implements(IProvidersSchema)

    enabled_portal_types = ProxyFieldProperty(IProvidersSchema['enabled_portal_types'])
    typebutton = ProxyFieldProperty(IProvidersSchema['typebutton'])


class TwitterControlPanelAdapter(BaseControlPanelAdapter):
    """ Twitter control panel adapter """
    adapts(IPloneSiteRoot)
    implements(ITwitterSchema)

    twitter_enabled = ProxyFieldProperty(ITwitterSchema['twitter_enabled'])
    twittvia = ProxyFieldProperty(ITwitterSchema['twittvia'])


class FbControlPanelAdapter(BaseControlPanelAdapter):
    """ Facebook control panel adapter """
    adapts(IPloneSiteRoot)
    implements(IFbSchema)

    fb_enabled = ProxyFieldProperty(IFbSchema['fb_enabled'])
    fbaction = ProxyFieldProperty(IFbSchema['fbaction'])
    fbadmins = ProxyFieldProperty(IFbSchema['fbadmins'])


class GpControlPanelAdapter(BaseControlPanelAdapter):
    """ Google+ control panel adapter """
    adapts(IPloneSiteRoot)
    implements(IGpSchema)

    gp_enabled = ProxyFieldProperty(IGpSchema['gp_enabled'])

baseset = FormFieldsets(IProvidersSchema)
baseset.id = 'baseset'
baseset.label = _(u'Base Plugin Configuration')

twitterset = FormFieldsets(ITwitterSchema)
twitterset.id = 'twitterset'
twitterset.label = _(u'Twitter settings')

fbset = FormFieldsets(IFbSchema)
fbset.id = 'fbset'
fbset.label = _(u'Facebook settings')

gpset = FormFieldsets(IGpSchema)
gpset.id = 'gpset'
gpset.label = _(u'Google+ settings')


class ProvidersControlPanel(ControlPanelForm):
    """ """
    form_fields = FormFieldsets(baseset, twitterset, fbset, gpset)

    form_fields['enabled_portal_types'].custom_widget = MultiSelectWidget

    label = _('Social: Like Actions settings')
    description = _('Configure settings for social like actions.')
    form_name = _('Social: Like Actions')
