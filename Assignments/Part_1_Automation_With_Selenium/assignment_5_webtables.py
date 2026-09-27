from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://demoqa.com/webtables")

try:
    # Locate the table body rows
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    target_first_name = "Cierra"
    found_salary = None
    found_department = None

    # Iterate through each row
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        # Column order: FirstName, LastName, Age, Email, Salary, Department, Action
        if cols[0].text == target_first_name:
            found_salary = cols[4].text
            found_department = cols[5].text
            break

    if found_salary:
        print(f"PASS: {target_first_name} -> Salary: {found_salary}, Department: {found_department}")
    else:
        print(f"FAIL: {target_first_name} not found in table")

except Exception as e:
    print("ERROR:", e)

finally:
    driver.quit()