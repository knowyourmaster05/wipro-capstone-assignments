from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

driver = webdriver.Chrome()
driver.get("https://demoqa.com/alerts")

try:
    # 1. JS Alert -> accept
    driver.find_element(By.ID, "alertButton").click()
    Alert(driver).accept()
    print("Accepted JS Alert")

    # 2. JS Confirm -> dismiss
    driver.find_element(By.ID, "confirmButton").click()
    Alert(driver).dismiss()
    print("Dismissed JS Confirm")

    # 3. JS Prompt -> send keys and accept
    driver.find_element(By.ID, "promtButton").click()
    alert = Alert(driver)
    alert.send_keys("1, 2, 3, 4")
    alert.accept()
    print("Entered text into JS Prompt and accepted")

except Exception as e:
    print("ERROR:", e)

finally:
    driver.quit()