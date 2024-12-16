from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from webdriver_manager.chrome import ChromeDriverManager

def safe_find_element(driver, by, value, timeout=10):
    """Safely find element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print(f"Error locating element {value}: {e}")
        return None

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.local.ch/en/d/lugano/6900/hairdresser/be-different-hairstyle-RfmOkYFPSMvDw6g7FuSqrg")
driver.maximize_window()

# Handle privacy modal
try:
    accept_button = safe_find_element(driver, By.XPATH, '//button[text()="I Accept"]')
    if accept_button:
        accept_button.click()
        print("Privacy modal accepted.")
except Exception as e:
    print(f"Failed to handle privacy modal: {e}")

# Data storage
salon_data = {}

# Scraping logic
try:
    # Name
    name_elem = safe_find_element(driver, By.CLASS_NAME, "DetailHeaderRow_title__d1OK")
    salon_data["Name"] = name_elem.text.strip() if name_elem else "N/A"

    # Address
    address_elems = driver.find_elements(By.XPATH, '//div[contains(@class, "DetailMapPreview_addressValue")]')
    salon_data["Address"] = " ".join([elem.text.strip() for elem in address_elems if elem.text.strip()])

    # Mobile Number
    mobile_elem = safe_find_element(driver, By.XPATH, '//a[contains(@href, "tel:") and contains(@class, "contactLink")]')
    salon_data["Mobile"] = mobile_elem.text.strip().replace('*', '') if mobile_elem else "N/A"

    # Email
    email_elem = safe_find_element(driver, By.XPATH, '//a[contains(@href, "mailto:")]')
    salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"

    # Categories
    category_elems = driver.find_elements(By.XPATH, '//a[contains(@class, "DescriptionContent_descriptionLinks")]')
    salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]

    # Opening Times
    opening_times = {}
    try:
        # Locate all the day blocks
        day_blocks = driver.find_elements(By.XPATH, '//li[@data-cy="opening-hours-weekdays"]')

        for block in day_blocks:
            try:
                # Extract the day name
                day_name = block.find_element(By.XPATH, './/span[contains(@class, "TimeFrame_day")]').text.strip()

                # Extract the opening hours
                hours = block.find_element(By.XPATH, './/div[@itemprop="openingHours"]').text.strip()

                # Add day and hours to the dictionary
                opening_times[day_name] = hours
            except Exception as e:
                print(f"Error processing day block: {e}")
    except Exception as e:
        print(f"Error locating opening times: {e}")

    salon_data["Opening Times"] = opening_times

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

# Save data to JSON
output_filename = "salon_datatest.json"
with open(output_filename, "w") as json_file:
    json.dump(salon_data, json_file, indent=4)
print(f"Data saved to {output_filename}.")
