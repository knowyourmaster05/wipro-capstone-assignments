from selenium.webdriver.common.by import By
from base_page import BasePage


class LoginPage(BasePage):
    # Only locators and UI methods here — no assertions
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.XPATH, "//input[@id='login-button']")

    URL = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        self.type(*self.USERNAME, username)
        self.type(*self.PASSWORD, password)
        self.click(*self.LOGIN_BTN)