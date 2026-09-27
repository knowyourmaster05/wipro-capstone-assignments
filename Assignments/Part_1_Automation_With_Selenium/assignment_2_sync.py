from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://demoqa.com/dynamic-properties")

try:
    wait = WebDriverWait(driver, 10)
    # This element becomes visible only after 5 seconds
    button = wait.until(EC.visibility_of_element_located((By.ID, "visibleAfter")))
    print("PASS: Element appeared after wait ->", button.text)
except Exception as e:
    print("ERROR:", e)
finally:
    driver.quit()