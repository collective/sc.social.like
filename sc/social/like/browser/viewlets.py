from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import ViewletBase

from sc.social.like.config import FB_LOCALES


def fix_iso(code):
    #TODO: We should be dealing also with *simple*
    #      language codes like pt or en or es
    if code.find('-') > -1:
        # we have a iso code like pt-br and FB_LOCALES uses pt_BR
        code = code.split('-')
        code = '%s_%s' % (code[0], code[1].upper())
    return code


def facebook_language(languages, default):
    """Given the prefered language on request we return the right
    language_code option to the template
    """
    if not languages:
        # do not change anything
        return default
    languages = [fix_iso(l) for l in languages]
    prefered = [l for l in languages if l in FB_LOCALES]
    return prefered and prefered[0] or default


class BaseLikeViewlet(ViewletBase):

    enabled_portal_types = []
    typebutton = ''
    twitter_enabled = False
    twittvia = ''
    fb_enabled = False
    fbaction = ''
    fbadmins = ''
    gp_enabled = False
    language = 'en_US'

    def __init__(self, context, request, view, manager):
        super(BaseLikeViewlet, self).__init__(context, request, view, manager)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        languages = self.request.get('HTTP_ACCEPT_LANGUAGE', '').split(';')[0].split(',')
        self.language = facebook_language(languages, self.language)
        self.site_url = self.portal_state.portal_url()
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        if self.sheet:
            self.enabled_portal_types = self.sheet.getProperty("enabled_portal_types", [])
            self.typebutton = self.sheet.getProperty("typebutton", "")
            self.twitter_enabled = self.sheet.getProperty("twitter_enabled", True)
            self.twittvia = self.sheet.getProperty("twittvia", "")
            self.fb_enabled = self.sheet.getProperty("fb_enabled", True)
            self.fbaction = self.sheet.getProperty("fbaction", "")
            self.fbadmins = self.sheet.getProperty("fbadmins", "")
            self.gp_enabled = self.sheet.getProperty("gp_enabled", True)

    def enabled(self):
        """Validates if the viewlet should be enabled for this context
        """
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types

    # HACK: fixes https://bitbucket.org/takaki/sc.social.like/issue/1
    def update(self):
        """Overriding ViewletBase because we may be called for
        UnauthorizedBinding objects
        """
        return


class SocialMetadataViewlet(BaseLikeViewlet):
    """Viewlet used to insert metadata into page header
    """
    render = ViewPageTemplateFile("templates/metadata.pt")

    def hasImage(self):
        """Return object image
        """
        context = self.context
        try:
            image = context.getField('image').get(context)
        except:
            image = ''

        try:
            return image.getSize() > 0
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


class SocialLikesViewlet(BaseLikeViewlet):
    """Viewlet used to display the buttons
    """
    render = ViewPageTemplateFile("templates/sociallikes.pt")
