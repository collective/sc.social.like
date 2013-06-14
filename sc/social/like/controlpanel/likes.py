# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFDefault.formlib.schema import ProxyFieldProperty as PFP
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like import LikeMessageFactory as _
from sc.social.like.plugins import IPlugin
from zope import schema
from zope.app.form.browser import itemswidgets
from zope.component import adapts
from zope.component import getUtilitiesFor
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.interface import Interface

CONTENT_TYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'


class MultiSelectWidget(itemswidgets.MultiSelectWidget):
    """ """
    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiSelectWidget, self).__init__(field,
                                                field.value_type.vocabulary,
                                                request)


class IProvidersSchema(Interface):
    """ General Configurations """

    enabled_portal_types = schema.Tuple(
        title=_(u'Content types'),
        description=_(
            u'help_portal_types',
            default=u"Please select content types in which the "
                    u"viewlet will be applied.",
        ),
        required=True,
        value_type=schema.Choice(vocabulary=CONTENT_TYPES)
    )

    plugins_enabled = schema.Tuple(
        title=_(u'Plugins'),
        description=_(
            u'help_enabled_plugins',
            default=u"Please select which plugins will be used",
        ),
        required=False,
        value_type=schema.Choice(vocabulary='sc.social.likes.plugins')
    )

    typebutton = schema.Choice(
        title=_(u'Button style'),
        description=_(
            u'help_selected_buttons',
            default=u"Choose your button style.",
        ),
        required=True,
        default=_(u'horizontal'),
        values=(_(u'horizontal'), _(u'vertical')),
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

    enabled_portal_types = PFP(IProvidersSchema['enabled_portal_types'])
    typebutton = PFP(IProvidersSchema['typebutton'])
    plugins_enabled = PFP(IProvidersSchema['plugins_enabled'])


class ProvidersControlPanel(ControlPanelForm):
    """ """
    template = ViewPageTemplateFile('likes.pt')
    form_fields = FormFields(IProvidersSchema)

    form_fields['enabled_portal_types'].custom_widget = MultiSelectWidget
    form_fields['plugins_enabled'].custom_widget = MultiSelectWidget

    label = _('Social: Like Actions settings')
    description = _('Configure settings for social like actions.')
    form_name = _('Social: Like Actions')

    def plugins_configs(self):
        ''' Return Plugins and their configuration pages '''
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
