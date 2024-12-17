from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from webdriver_manager.chrome import ChromeDriverManager

def safe_find_element(driver, by, value, timeout=10, condition=EC.presence_of_element_located):
    """Safely find element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            condition((by, value))
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
    # Name Extraction
    name_elem = safe_find_element(driver, By.XPATH, '//h1[contains(@class, "DetailHeaderRow_title")]', timeout=10, condition=EC.visibility_of_element_located)
    salon_data["Name"] = name_elem.text.strip() if name_elem else "N/A"
    print(f"Name: {salon_data['Name']}")

    # Address Extraction
    address_elem = safe_find_element(driver, By.XPATH, '//a[contains(@class, "DetailMapPreview_addressValue")]')
    if address_elem:
        address_parts = [part.strip() for part in address_elem.text.split("\n") if part.strip()]
        salon_data["Address"] = address_parts
    else:
        salon_data["Address"] = ["N/A"]
    print(f"Address: {salon_data['Address']}")

    # Mobile Number Extraction
    mobile_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "tel:")]')
    salon_data["Mobile"] = mobile_elem.text.strip().replace("*", "") if mobile_elem else "N/A"
    print(f"Mobile: {salon_data['Mobile']}")

    # Email Extraction
    email_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "mailto:")]')
    salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"
    print(f"Email: {salon_data['Email']}")

    # Categories Extraction
    categories_container = safe_find_element(driver, By.XPATH, '//dt[contains(text(), "Categories")]/following-sibling::dd')
    if categories_container:
        category_elems = categories_container.find_elements(By.TAG_NAME, "a")
        salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]
    else:
        salon_data["Categories"] = []
    print(f"Categories: {salon_data['Categories']}")

    # Opening Times
    opening_times = {}
    try:
        day_blocks = driver.find_elements(By.XPATH, '//li[@data-cy="opening-hours-weekdays"]')
        for block in day_blocks:
            try:
                day_name = block.find_element(By.XPATH, './/span[contains(@class, "TimeFrame_day")]').text.strip()
                hours = block.find_element(By.XPATH, './/div[@itemprop="openingHours"]').text.strip().replace("\n to \n", " - ")
                opening_times[day_name] = hours
            except Exception as e:
                print(f"Error processing day block: {e}")
    except Exception as e:
        print(f"Error locating opening times: {e}")

    salon_data["Opening Times"] = opening_times
    print(f"Opening Times: {salon_data['Opening Times']}")

    # Rating Extraction using data-testid
    rating_elem = safe_find_element(driver, By.XPATH, '//span[@data-testid="average-rating"]')
    if rating_elem:
        rating_parts = [part.strip() for part in rating_elem.text.split("\n") if part.strip()]
        salon_data["Rating"] = rating_parts[0] if rating_parts else "N/A"  # Extract and clean the rating
    else:
        salon_data["Rating"] = "N/A"
    print(f"Rating: {salon_data['Rating']}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

# Save data to JSON
output_filename = "salon_data.json"
with open(output_filename, "w") as json_file:
    json.dump(salon_data, json_file, indent=4)
print(f"Data saved to {output_filename}.")
