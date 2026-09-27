*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open Browser And Login
    Open Browser    https://www.saucedemo.com/    chrome
    Maximize Browser Window
    Input Text      id:user-name    standard_user
    Input Text      id:password     secret_sauce
    Click Button    id:login-button
    Wait Until Element Is Visible    class:inventory_list    timeout=10s
    Page Should Contain Element      class:inventory_list
    Close Browser