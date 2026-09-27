*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}       https://www.saucedemo.com/
${BROWSER}   chrome

*** Test Cases ***
Login Using Custom Keywords
    Open Browser To Login Page
    Enter Credentials    standard_user    secret_sauce
    Verify Login Success
    [Teardown]    Close Browser

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Enter Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id:user-name    ${username}
    Input Text    id:password     ${password}
    Click Button    id:login-button

Verify Login Success
    Page Should Contain Element    class:inventory_list