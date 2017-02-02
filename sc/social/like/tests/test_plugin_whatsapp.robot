*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${title_selector} =  input#title,input#form-widgets-IDublinCore-title
${whatsapp_locator}  css=#viewlet-social-like .whatsapp.active

*** Test cases ***

Test Desktop Version
    Open Test Browser
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create NewsItem  Extra! Extra!
    Page Should Not Contain Element  ${whatsapp_locator}
    Close all browsers

Test Mobile Version
    [Tags]  Expected Failure

    Open Mobile Test Browser
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create NewsItem  Extra! Extra!
    Page Should Contain Element  ${whatsapp_locator}
    Close all browsers

*** Keywords ***

Open Mobile Test Browser
    Open browser  ${START_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES}
    ...           ff_profile_dir=.

Click Add NewsItem
    Open Add New Menu
    Click Link  css=a#news-item
    Page Should Contain  Add News Item

Create NewsItem
    [arguments]  ${title}

    Click Add NewsItem
    Input Text  css=${title_selector}  ${title}
    Click Button  Save
    Page Should Contain  ${title}
