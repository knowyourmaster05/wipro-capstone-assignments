from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup Driver (Chrome)
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.saucedemo.com/")

try:
    # 1. Find username field using By.ID
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")

    # 2. Find password field using By.NAME
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("secret_sauce")

    # 3. Find login button using By.XPATH
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    login_button.click()

    # Validation
    time.sleep(2)
    current_url = driver.current_url
    if "inventory.html" in current_url:
        print("Validation Passed: URL contains inventory.html")
    else:
        print(f"Validation Failed: URL is {current_url}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()