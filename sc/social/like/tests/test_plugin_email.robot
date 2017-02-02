*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote
Library  ${CURDIR}/ManagePluginUtils.py

*** Variables ***

${title_selector} =  input#title,input#form-widgets-IDublinCore-title
${email_locator} =  css=#viewlet-social-like .share-by-email
${send_to_selector} =  css=#send_to_address
${send_from_selector} =  css=#send_from_address
${email} =  admin@plone.org

*** Test cases ***

Test Email Plugin
    Open Test Browser
    Enable Autologin as  Site Administrator
    Enable Plugin  Email
    Go to Homepage
    Create Document  Extra! Extra!
    Publish Content
    Wait until keyword succeeds  1  5  Element Should Be Visible  ${email_locator}
    Sleep  1s  Wait for social like to load
    Click Link  ${email_locator}
    Input Text  ${send_to_selector}  ${email}
    Input Text  ${send_from_selector}  ${email}
    Click Button  Send
    Page Should not Contain Element  css=.portalMessage.error
    Close all browsers

*** Keywords ***

Click Add Document
    Open Add New Menu
    Click Link  css=a#document
    Wait until page contains  Add Page

Create Document
    [arguments]  ${title}

    Click Add Document
    Input Text  css=${title_selector}  ${title}
    Click Button  Save
    Page Should Contain  ${title}

Open Workflow Menu
    Sleep  1s  Wait for contentmenu to load
    Open Menu  plone-contentmenu-workflow

Publish Content
    Open Workflow Menu
    Click Link  css=a#workflow-transition-publish
