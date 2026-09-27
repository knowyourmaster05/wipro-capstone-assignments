import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    # Fixture handles setup
    d = webdriver.Chrome()
    d.get("https://www.saucedemo.com/")
    yield d
    # Fixture handles teardown
    d.quit()


def test_page_title(driver):
    assert "Swag Labs" in driver.title


def test_login_button_visible(driver):
    assert driver.find_element(By.ID, "login-button").is_displayed()


def test_username_field_visible(driver):
    assert driver.find_element(By.ID, "user-name").is_displayed()


def test_password_field_visible(driver):
    assert driver.find_element(By.NAME, "password").is_displayed()