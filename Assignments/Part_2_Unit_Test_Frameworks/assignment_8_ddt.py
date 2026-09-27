import csv
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


# Load test data from external CSV
def load_test_data():
    csv_path = os.path.join(os.path.dirname(__file__), "testdata.csv")
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.get("https://www.saucedemo.com/")
    yield d
    d.quit()


@pytest.mark.parametrize("row", load_test_data())
def test_login_ddt(driver, row):
    driver.find_element(By.ID, "user-name").send_keys(row["username"])
    driver.find_element(By.NAME, "password").send_keys(row["password"])
    driver.find_element(By.ID, "login-button").click()

    if row["expected"] == "success":
        assert "inventory.html" in driver.current_url
    else:
        # Validation error should appear
        error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert "Epic sadface" in error