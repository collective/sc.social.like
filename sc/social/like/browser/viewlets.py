from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.publisher.interfaces import IPublishTraverse
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from string import Template
import sre


class SocialMetadataViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile("templates/metadata.pt")

    def __init__(self, context, request, view, manager):
        super(SocialMetadataViewlet, self).__init__(context, request, view, manager)
        pp = getToolByName(context,'portal_properties')

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.sheet = getattr(pp,'sc_social_likes_properties',None)
        if self.sheet:
            self.enabled_portal_types = self.sheet.getProperty("enabled_portal_types") or []
            self.fbadmins = self.sheet.getProperty("fbadmins") or ''
        else:
            self.enabled_portal_types = []
            self.fbadmins = ''

    def fbadmins(self):
        """Return admins comma-separated
        """
        fbadmins = self.fbadmins
        return fbadmins

    def enabled(self):
        """Validates if the viewlet should be enabled
           for this context"""
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types

    def hasImage(self):
        """Return object image
        """
        context = self.context
        try:
            image = context.getField('image').get(context)
        except:
            image = ''

        try:
            return image.getSize()>0
        except:
            return bool(image)

    def portaltitle(self):
        """Return the portal title
        """
        portaltitle = self.portal_state.portal_title()

        return portaltitle

    def logoname(self):
        """Return portal logo name
        """
        portal = self.portal_state.portal()
        bprops = portal.restrictedTraverse('base_properties', None)
        if bprops is not None:
            logoName = bprops.logoName
        else:
            logoName = 'logo.png'

        return logoName

class SocialLikesViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile("templates/sociallikes.pt")
   
    def __init__(self, context, request, view, manager):
        super(SocialLikesViewlet, self).__init__(context, request, view, manager)
        pp = getToolByName(context,'portal_properties')
        self.sheet = getattr(pp,'sc_social_likes_properties',None)
        if self.sheet:
            self.enabled_portal_types = self.sheet.getProperty("enabled_portal_types") or []
            self.typebutton = self.sheet.getProperty("typebutton") or ''
            self.twittvia = self.sheet.getProperty("twittvia") or ''
            self.fbaction = self.sheet.getProperty("fbaction") or ''
            self.fbadmins = self.sheet.getProperty("fbadmins") or ''
        else:
            self.enabled_portal_types = []
            self.typebutton = ''
            self.twittvia = ''
            self.fbaction = ''
            self.fbadmins = ''

    def enabled(self):
        """Validates if the viewlet should be enabled
           for this context"""
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types

    def typebutton(self):
        """
        """
        typebutton = self.typebutton
        return typebutton

    def twittvia(self):
        """
        """
        twittvia = self.twittvia
        return twittvia

    def fbaction(self):
        """
        """
        fbaction = self.fbaction
        return fbaction

    def fbadmins(self):
        """Return admins comma-separated
        """
        fbadmins = self.fbadmins
        return fbadmins
