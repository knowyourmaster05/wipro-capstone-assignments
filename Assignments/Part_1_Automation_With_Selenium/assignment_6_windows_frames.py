from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://demoqa.com/frames")

try:
    original_window = driver.current_window_handle

    # --- Step 1: Interact with elements inside iframe ---
    iframe = driver.find_element(By.ID, "frame1")
    driver.switch_to.frame(iframe)
    heading = driver.find_element(By.ID, "sampleHeading").text
    print("Inside iframe, heading text:", heading)

    # Return to main page
    driver.switch_to.default_content()
    print("Switched back to main layout")

    # --- Step 2: Open a new tab ---
    driver.execute_script("window.open('https://demoqa.com/browser-windows');")
    
    # Switch to the newly opened tab
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break

    print("New tab title:", driver.title)

    # Grab the new tab's content
    new_tab_heading = driver.find_element(By.TAG_NAME, "h1").text
    print("New tab heading:", new_tab_heading)

    # Close the new tab
    driver.close()

    # Switch back to original window
    driver.switch_to.window(original_window)
    print("Back to main tab, title:", driver.title)

except Exception as e:
    print("ERROR:", e)

finally:
    driver.quit()