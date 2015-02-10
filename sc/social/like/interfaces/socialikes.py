from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('sc.social.like')


class ISocialLikeLayer(Interface):
    """
    """


class ISocialLikes(Interface):
    """
    """


class IHelperView(Interface):
    """
    """
    def configs():
        ''' Social Like configuration '''

    def enabled_portal_types():
        ''' Portal Types that will display our viewlet '''

    def plugins_enabled():
        ''' List of plugins enabled '''

    def typebutton():
        ''' Button to be used '''

    def enabled(view):
        '''
        Social Like is enabled for this context and provided view
        (when provided)
        '''

    def available_plugins():
        ''' Return available plugins '''

    def plugins():
        ''' Return enabled plugins '''

    def view_template_id():
        ''' View or template id for this context '''
