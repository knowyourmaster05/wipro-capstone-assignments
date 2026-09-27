from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By


@given("I open the SauceDemo login page")
def step_open_login(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.saucedemo.com/")


@when("I enter valid credentials")
def step_valid_credentials(context):
    context.driver.find_element(By.ID, "user-name").send_keys("standard_user")
    context.driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    context.driver.find_element(By.ID, "login-button").click()


@when("I enter invalid credentials")
def step_invalid_credentials(context):
    context.driver.find_element(By.ID, "user-name").send_keys("wrong_user")
    context.driver.find_element(By.NAME, "password").send_keys("wrong_pass")
    context.driver.find_element(By.ID, "login-button").click()


@then("the URL should contain inventory.html")
def step_check_url(context):
    assert "inventory.html" in context.driver.current_url
    context.driver.quit()


@then("I should see an error message")
def step_check_error(context):
    error = context.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "Epic sadface" in error
    context.driver.quit()