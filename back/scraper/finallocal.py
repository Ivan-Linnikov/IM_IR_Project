from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from webdriver_manager.chrome import ChromeDriverManager

MAX_PAGE_LIMIT = 60  

def safe_find_element(driver, by, value, timeout=5):
    """Safely find an element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception:
        return None
    
def safe_find_element1(driver, by, value, timeout=1):
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
        name_elem = safe_find_element1(driver, By.XPATH, '//h1[contains(@class, "DetailHeaderRow_title")]')
        salon_data["Name"] = name_elem.text.strip() if name_elem else "N/A"

        address_elem = safe_find_element1(driver, By.XPATH, '//a[contains(@class, "DetailMapPreview_addressValue")]')
        salon_data["Address"] = address_elem.text.strip() if address_elem else "N/A"

        mobile_elem = safe_find_element1(driver, By.XPATH, '//a[starts-with(@href, "tel:")]')
        salon_data["Mobile"] = mobile_elem.text.strip().replace("*", "") if mobile_elem else "N/A"

        email_elem = safe_find_element1(driver, By.XPATH, '//a[starts-with(@href, "mailto:")]')
        salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"

        categories_container = safe_find_element1(driver, By.XPATH, '//dt[contains(text(), "Categories")]/following-sibling::dd')
        if categories_container:
            category_elems = categories_container.find_elements(By.TAG_NAME, "a")
            salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]
        else:
            salon_data["Categories"] = ["Missing"]

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

def click_next_button(driver, retries=3):
    """Attempts to click the 'Next' button, with retries."""
    next_button_xpath = '//button[@id="load-next-page"]'
    for attempt in range(retries):
        try:
            next_button = safe_find_element(driver, By.XPATH, next_button_xpath, timeout=3)
            if next_button and next_button.is_enabled():
                print(f"Clicking next button... (Attempt {attempt + 1})")
                next_button.click()
                time.sleep(2) 
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1} to click 'Next' button failed: {e}")
        time.sleep(1)
    return False

def go_to_previous_page(driver):
    """Clicks the previous page button to navigate back."""
    previous_button_xpath = '//button[contains(@class, "Pagination_navigationButtonPrev")]'
    try:
        prev_button = safe_find_element(driver, By.XPATH, previous_button_xpath, timeout=3)
        if prev_button and prev_button.is_enabled():
            print("Clicking previous button to retry navigation...")
            prev_button.click()
            time.sleep(2)
            return True
    except Exception as e:
        print(f"Failed to navigate to the previous page: {e}")
    return False

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.local.ch/en/s/Hairdresser?rid=b69308&page=91")

try:
    accept_button = safe_find_element(driver, By.XPATH, '//button[text()="I Accept"]')
    if accept_button:
        accept_button.click()
        print("Privacy modal accepted.")
except Exception:
    pass

all_salon_data = []
page_number = 1


while page_number <= MAX_PAGE_LIMIT:
    try:
        print(f"Scraping page {page_number}...")

        salon_links = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "ListElement_link")]'))
        )
        salon_urls = [link.get_attribute("href") for link in salon_links]

        print(f"Found {len(salon_urls)} salons on page {page_number}.")

        for idx, url in enumerate(salon_urls, start=1):
            print(f"Opening salon {idx} on page {page_number}...")
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)

                salon_data = scrape_salon_page(driver)
                all_salon_data.append(salon_data)
                print(f"Scraped salon {idx}: {salon_data.get('Name', 'N/A')}")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error processing salon {idx}: {e}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        if not click_next_button(driver):
            print("Failed to click the 'Next' button. Attempting to retry from the previous page...")
            if go_to_previous_page(driver):  
                print("Retrying to click the 'Next' button from the previous page...")
                if not click_next_button(driver):  
                    print("Retry failed. Exiting...")
                    break
            else:
                print("Could not navigate to the previous page. Exiting...")
                break
        page_number += 1

    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")
        break


driver.quit()

output_filename = "final_all_salon_data_after_91.json"
with open(output_filename, "w") as json_file:
    json.dump(all_salon_data, json_file, indent=4)

