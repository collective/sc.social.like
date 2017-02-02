*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${title_selector} =  input#title,input#form-widgets-IDublinCore-title
${telegram_locator}  css=#viewlet-social-like .telegram

*** Test cases ***

Test Telegram
    [Tags]  Expected Failure

    Open Test Browser
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create NewsItem  Extra! Extra!
    Page Should Contain Element  ${telegram_locator}
    Close all browsers

*** Keywords ***

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
