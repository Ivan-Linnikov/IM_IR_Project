from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

def safe_find_element(driver, by, value, timeout=5):
    """Safely find an element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception:
        return None

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.herold.at/gelbe-seiten/feldkirch/3x7VW/crimpers-for-your-hair-inh-udo-neyer/" 

try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='cmpbntyestxt' and text()='Alle akzeptieren']"))
    )
    if accept_button:
        accept_button.click()
        print("Privacy modal accepted.")
except Exception as e:
    print(f"Error handling privacy modal: {e}")

def scrape_page_name(driver):
    """Function to scrape the page name."""
    try:
        name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='text-lg font-black md:text-2xl lg:text-3xl']"))
        )
        name = name_elem.text.strip()
        return name
    except Exception as e:
        print(f"Error: {e}")
        return "N/A"

def scrape_address(driver):
    """Function to scrape the address."""
    try:
        address_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='contents']"))
        )
        address = address_elem.text.strip()
        return address
    except Exception as e:
        print(f"Error: {e}")
        return "N/A"

def scrape_phone_number(driver):
    """Function to scrape the phone number."""
    try:
        phone_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@itemprop='telephone']"))
        )
        phone_number = phone_elem.get_attribute("href").replace("tel:", "").strip()
        return phone_number
    except Exception as e:
        print(f"Error: {e}")
        return "N/A"

page_name = scrape_page_name(driver)
address = scrape_address(driver)
phone_number = scrape_phone_number(driver)

data = {
    "Page Name": page_name,
    "Address": address,
    "Phone Number": phone_number
}
output_filename = "page_details.json"
with open(output_filename, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data saved to {output_filename}: {data}")

driver.quit()
