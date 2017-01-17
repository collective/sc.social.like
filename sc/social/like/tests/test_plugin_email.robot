*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote
Library  ${CURDIR}/ManagePluginUtils.py

*** Variables ***

${title_selector} =  input#title
${email_locator}  css=#viewlet-social-like .share-by-email

*** Test cases ***

Test Email Plugin
    Open Test Browser
    Enable Autologin as  Site Administrator
    Enable Plugin  Email
    Go to Homepage
    Create Document  Extra! Extra!
    Publish Content
    Wait until page contains  ${email_locator}
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
    Page Should Contain  Changes saved.

Open Workflow Menu
    Open Menu  plone-contentmenu-workflow

Publish Content
    Open Workflow Menu
    Click Link  css=a#workflow-transition-publish
