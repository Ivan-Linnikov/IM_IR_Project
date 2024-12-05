from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def safe_find_element(driver, by, value, timeout=10):
    """Find an element with explicit wait and return None if not found."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print(f"Error locating element {value}: {e}")
        return None

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.local.ch/en/s/Hairdresser%2C%20lugano?rid=f87043")
driver.maximize_window()

# Handle privacy modal
try:
    accept_button = safe_find_element(driver, By.XPATH, '//button[text()="I Accept"]')
    if accept_button:
        accept_button.click()
        print("Privacy modal accepted.")
except Exception as e:
    print(f"Failed to handle privacy modal: {e}")

# Initialize data storage
salon_names = []
addresses = []
closing_times = []

# Scrape data
page_number = 1
while True:
    try:
        print(f"Scraping page {page_number}...")

        # Wait for the result list to load
        results_container = safe_find_element(driver, By.XPATH, '//div[contains(@class, "SearchResultList_listElementWrapper")]')
        if not results_container:
            print(f"Could not find results on page {page_number}. Exiting...")
            break

        # Get all salon results
        salons = driver.find_elements(By.XPATH, '//div[contains(@class, "SearchResultList_listElementWrapper")]')
        print(f"Found {len(salons)} salons on page {page_number}.")

        for idx, salon in enumerate(salons, start=1):
            try:
                # Salon name
                name_elem = salon.find_element(By.XPATH, './/h2[contains(@class, "ListElement_titleHeadline__sAf_l")]')
                name = name_elem.text if name_elem else "N/A"

                # Address
                address_elem = salon.find_element(By.XPATH, './/address')
                address = address_elem.text if address_elem else "N/A"

                # Closing time
                closing_time_elem = salon.find_element(By.XPATH, './/section[@data-testid="open-label"]')
                closing_time = closing_time_elem.text if closing_time_elem else "N/A"

                # Store data
                salon_names.append(name)
                addresses.append(address)
                closing_times.append(closing_time)

                # Print the data for verification
                print(f"Salon {idx} on page {page_number}:")
                print(f"  Name: {name}")
                print(f"  Address: {address}")
                print(f"  Closing Time: {closing_time}")
            except Exception as e:
                print(f"Error processing salon {idx} on page {page_number}: {e}")

        # Try to navigate to the next page
        try:
            # Re-locate the "Next" button to avoid stale element reference issues
            next_button_xpath = '//button[@id="load-next-page"]'
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
            if next_button:
                next_button.click()
                print(f"Moving to page {page_number + 1}...")
                page_number += 1
                time.sleep(3)  # Allow time for the next page to load
            else:
                print("No more pages to scrape or 'Next' button is disabled.")
                break
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")
        break

# Close the WebDriver
driver.quit()

# Save the data to a CSV
csv_filename = "local_ch_hairdressers_lugano.csv"
data = pd.DataFrame({
    "Salon Name": salon_names,
    "Address": addresses,
    "Closing Time": closing_times
})
data.to_csv(csv_filename, index=False)
print(f"Scraping complete. Data saved to {csv_filename}")
