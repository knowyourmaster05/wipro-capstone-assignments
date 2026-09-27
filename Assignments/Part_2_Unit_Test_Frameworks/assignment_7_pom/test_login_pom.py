import pytest
from selenium import webdriver
from login_page import LoginPage


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()


def test_valid_login(driver):
    # Test logic / assertions live HERE, not in the page class
    page = LoginPage(driver).open()
    page.login("standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


def test_invalid_login(driver):
    page = LoginPage(driver).open()
    page.login("wrong_user", "wrong_pass")
    assert "inventory.html" not in driver.current_url