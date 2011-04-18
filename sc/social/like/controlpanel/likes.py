from zope.schema import Int
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

from zope.formlib.form import FormFields
from plone.app.controlpanel.form import ControlPanelForm
from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget as BaseOrderedMultiSelectWidget
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget, MultiCheckBoxVocabularyWidget

from sc.social.like import LikeMessageFactory as _

class MultiSelectWidget(BaseMultiSelectWidget):
    """ """
    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiSelectWidget, self).__init__(field,
            field.value_type.vocabulary, request)
           
class IProvidersSchema(Interface):
    """ """ 
    enabled_portal_types = Tuple(
        title=_(u'Content types'),
        description=_(u'help_portal_types',
            default=u"Please select content types in which the viewlet will be applied.",
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
        values=(_(u'horizontal'),_(u'vertical')),
    )

    twittvia = TextLine(
        title=_(u'Twitter nick'),
        description=_(u'help_your_twitter_nick',
            default=u"Enter your twitter nick. eg. simplesconsultoria",
        ),
        required=False,
    )

    fbaction = Choice(
        title=_(u'Verb to display'),
        description=_(u'help_verb_display',
            default=u"The verb to display in the facebook button. Currently only 'like' and 'recommend' are supported.",
        ),
        required=True,
        default=u'like',
        values=(_(u'like'),_(u'recommend')),
    )
  
    fbadmins = TextLine(
        title=_(u'Admins'),
        description=_(u'help_admins',
            default=u"A comma-separated list of either the Facebook IDs of page administrators or a Facebook Platform application ID.",
        ),
        required=False,
    )
 
class ProvidersControlPanelAdapter(SchemaAdapterBase):
    """ """
    adapts(IPloneSiteRoot)
    implements(IProvidersSchema)
   
    def __init__(self, context):
        super(ProvidersControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.sc_social_likes_properties
   
    enabled_portal_types = ProxyFieldProperty(IProvidersSchema['enabled_portal_types'])
    typebutton = ProxyFieldProperty(IProvidersSchema['typebutton'])
    twittvia = ProxyFieldProperty(IProvidersSchema['twittvia'])
    fbaction = ProxyFieldProperty(IProvidersSchema['fbaction'])
    fbadmins = ProxyFieldProperty(IProvidersSchema['fbadmins'])

class ProvidersControlPanel(ControlPanelForm):
    """ """
    form_fields = FormFields(IProvidersSchema)
    form_fields['enabled_portal_types'].custom_widget = MultiSelectWidget


    label = _('Social: Like Actions settings')
    description = _('Configure settings for social like actions.')
    form_name = _('Social: Like Actions')
