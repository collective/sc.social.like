from Products.CMFCore.utils import getToolByName

def install(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('sc.social.like_install.txt') is None:
        return

    # Add additional setup code here

def uninstall(context):

    if context.readDataFile('sc.social.like_uninstall.txt') is None:
        return

    portal = context.getSite()
    portal_conf = getToolByName(portal, 'portal_controlpanel')
    portal_conf.unregisterConfiglet('@@likes-providers')

    # Remove tweetmeme_properties in portal properties
    pp = getToolByName('portal_properties')

    try:
        if hasattr(pp, 'sc_social_likes_properties'):
            pp.manage_delObjects(ids='sc_social_likes_properties')
    except KeyError:
        pass


def upgradefrom1001(context):
    ''' Upgrade from 1001
    '''
    setup = getToolByName(context, 'portal_setup')
    
    # Install
    profiles = ['profile-sc.social.like:to2000', ]
    
    for profile in profiles:
        setup.runAllImportStepsFromProfile(profile)
