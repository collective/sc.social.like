*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${title_selector} =  input#title,input#form-widgets-IDublinCore-title
${facebook_locator}  css=#viewlet-social-like .sociallike-network-facebook

*** Test cases ***

Test Hide Unpublished
    Open Test Browser
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Document  Extra! Extra!
    Element Should Not Be Visible  ${facebook_locator}
    Publish Content
    Wait until keyword succeeds  1  5  Element Should Be Visible  ${facebook_locator}
    Close all browsers

*** Keywords ***

Click Add Document
    Open Add New Menu
    Click Link  css=a#document
    Page Should Contain  Add Page

Create Document
    [arguments]  ${title}

    Click Add Document
    Input Text  css=${title_selector}  ${title}
    Click Button  Save
    Page Should Contain  ${title}

Open Workflow Menu
    Open Menu  plone-contentmenu-workflow

Publish Content
    Open Workflow Menu
    Click Link  css=a#workflow-transition-publish
