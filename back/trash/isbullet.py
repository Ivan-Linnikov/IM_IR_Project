from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from webdriver_manager.chrome import ChromeDriverManager

def safe_find_element(driver, by, value, timeout=5):
    """Safely find an element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception:
        return None

def scrape_salon_page(driver):
    """Scrapes data from an individual salon page."""
    salon_data = {}
    try:
        # Name
        name_elem = safe_find_element(driver, By.XPATH, '//h1[contains(@class, "DetailHeaderRow_title")]')
        salon_data["Name"] = name_elem.text.strip() if name_elem else "N/A"

        # Address
        address_elem = safe_find_element(driver, By.XPATH, '//a[contains(@class, "DetailMapPreview_addressValue")]')
        salon_data["Address"] = address_elem.text.strip() if address_elem else "N/A"

        # Mobile
        mobile_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "tel:")]')
        salon_data["Mobile"] = mobile_elem.text.strip().replace("*", "") if mobile_elem else "N/A"

        # Email
        email_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "mailto:")]')
        salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"

        # Categories
        categories_container = safe_find_element(driver, By.XPATH, '//dt[contains(text(), "Categories")]/following-sibling::dd')
        if categories_container:
            category_elems = categories_container.find_elements(By.TAG_NAME, "a")
            salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]
        else:
            salon_data["Categories"] = ["Missing"]

        # Opening Times
        opening_times = {}
        day_blocks = driver.find_elements(By.XPATH, '//li[@data-cy="opening-hours-weekdays"]')
        for block in day_blocks:
            day_name_elem = block.find_element(By.XPATH, './/span[contains(@class, "TimeFrame_day")]')
            hours_elem = block.find_element(By.XPATH, './/div[@itemprop="openingHours"]')
            day_name = day_name_elem.text.strip() if day_name_elem else "Missing"
            hours = hours_elem.text.strip() if hours_elem else "Missing"
            opening_times[day_name] = hours
        salon_data["Opening Times"] = opening_times if opening_times else {"Opening Hours": "Missing"}

    except Exception as e:
        print(f"Error scraping salon page: {e}")
    return salon_data

# Main Scraper
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.local.ch/en/s/Hairdresser%2C%20lugano?rid=4a3bb8")
driver.maximize_window()

# Handle privacy modal
try:
    accept_button = safe_find_element(driver, By.XPATH, '//button[text()="I Accept"]')
    if accept_button:
        accept_button.click()
        print("Privacy modal accepted.")
except Exception:
    pass

# Data storage
all_salon_data = []
page_number = 1

while True:
    try:
        print(f"Scraping page {page_number}...")

        # Locate salon links
        salon_links = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "ListElement_link")]'))
        )
        salon_urls = [link.get_attribute("href") for link in salon_links]
        print(f"Found {len(salon_urls)} salons on page {page_number}.")

        # Scrape data from each salon
        for idx, url in enumerate(salon_urls, start=1):
            print(f"Opening salon {idx} on page {page_number}...")
            try:
                # Open in new tab
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)

                salon_data = scrape_salon_page(driver)
                all_salon_data.append(salon_data)
                print(f"Scraped salon {idx}: {salon_data.get('Name', 'N/A')}")

                driver.close()  # Close new tab
                driver.switch_to.window(driver.window_handles[0])  # Return to list tab
                time.sleep(0.5)  # Small delay for stabilization

            except Exception as e:
                print(f"Error processing salon {idx}: {e}")
                driver.close()  # Close the tab in case of error
                driver.switch_to.window(driver.window_handles[0])

        # Check if fewer than 20 salons are present -> Last page
        if len(salon_urls) < 20:
            print("Detected last page. Exiting...")
            break

        # Navigate to the next page
        next_button_xpath = '//button[@id="load-next-page"]'
        next_button = None

        for _ in range(3):  # Retry locating the next button
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                )
                if next_button:
                    print("Clicking next button to go to next page...")
                    next_button.click()
                    page_number += 1
                    time.sleep(2)  # Allow time for page load
                    break
            except Exception:
                print("Next button not found or stale. Retrying...")
                time.sleep(2)
        else:
            print("No more pages found. Exiting...")
            break

    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")
        break

# Close the WebDriver
driver.quit()

# Save data to JSON
output_filename = "all_salon_data.json"
with open(output_filename, "w") as json_file:
    json.dump(all_salon_data, json_file, indent=4)

print(f"Data saved to {output_filename}.")
