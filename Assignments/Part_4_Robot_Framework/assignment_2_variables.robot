*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}       https://www.saucedemo.com/
${BROWSER}   chrome
${USER}      standard_user
${PASS}      secret_sauce

*** Test Cases ***
Login With Variables
    [Documentation]    Test using variables for data storage
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text      id:user-name    ${USER}
    Input Text      id:password     ${PASS}
    Click Button    id:login-button
    Page Should Contain Element    class:inventory_list
    Close Browser