import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


 # "https://www.cybo.com/LI-biz/fusspflege-in-mauren-martina-b%C3%BCchel",
    # "https://www.cybo.com/LI-biz/coiffeur-klaudia",
    # "https://www.cybo.com/LI-biz/salon-mano-anstalt",
    # "https://www.cybo.com/LI-biz/sie-er-coiffure",
    # "https://www.cybo.com/LI-biz/coiffeursalon-studio-haarscharf",
    # "https://www.cybo.com/LI-biz/estilo-libre-hair-beauty",
    # "https://www.cybo.com/LI-biz/tona-hairstyle",
    # "https://www.cybo.com/LI-biz/salon-niedhart-damen-und-herren",
    # "https://www.cybo.com/LI-biz/salon-astrid",
    # "https://www.cybo.com/LI-biz/studio-haar-kult-mauren",

    # "https://www.cybo.com/LI-biz/coiffeur-les-artistes",
    # "https://www.cybo.com/LI-biz/coiffure-fabrizio",
    # "https://www.cybo.com/LI-biz/gidor-coiffure-vaduz",
    # "https://www.cybo.com/LI-biz/a-kerhart-coiffeur-headroom_1C",
    # "https://www.cybo.com/LI-biz/haarlocke-frisuren-mehr",
    # "https://www.cybo.com/LI-biz/top-hair",
    # "https://www.cybo.com/LI-biz/secrets-of-beauty-est",
    # "https://www.cybo.com/LI-biz/big-coiffeur",
    # "https://www.cybo.com/LI-biz/coiffeursalon-herrensalon-vincenzo",
    # "https://www.cybo.com/LI-biz/a-kerhart-coiffeur-headroom",
    
    # "https://www.cybo.com/LI-biz/h%C3%A4%C3%A4r-%C3%A4nd-sch%C3%A4r",
    # "https://www.cybo.com/LI-biz/coiffeursalon-em",
    # "https://www.cybo.com/LI-biz/mrs-beatrice-w%C3%BCst-fusspflegesalon",


# # List of URLs
# SALON_URLS = [
#     "https://www.cybo.com/LI-biz/coiffeursalon-fris%C3%B6r",
#     "https://www.cybo.com/LI-biz/coiffure-zur-schmiede",
#     "https://www.cybo.com/LI-biz/salon-liz",
#     "https://www.cybo.com/LI-biz/erikas-fusspflegepraxis",
#     "https://www.cybo.com/LI-biz/designerama-hair-sabrina-malin",
#     "https://www.cybo.com/LI-biz/pakos-barbershop",
#     "https://www.cybo.com/LI-biz/haarzentrum",
#     "https://www.cybo.com/LI-biz/coiffeur-zur-schmiede",
#     "https://www.cybo.com/LI-biz/coiffeur-magic_10",
#     "https://www.cybo.com/LI-biz/ruths-scherenzauber",
#     "https://www.cybo.com/LI-biz/skinminded-laser-clinics",
#     "https://www.cybo.com/LI-biz/haarfrei-jetzt",
#     "https://www.cybo.com/LI-biz/birgit",
#     "https://www.cybo.com/LI-biz/hair-and-body",
#     "https://www.cybo.com/LI-biz/coiffeur-andrea",
#     "https://www.cybo.com/LI-biz/mrs-gerda-elkuch-fusspflegesalon_1R",
#     "https://www.cybo.com/LI-biz/adventure-coiffeur-manuela",
#     "https://www.cybo.com/LI-biz/corina",
#     "https://www.cybo.com/LI-biz/haarzentrum-lett_1b",
#     "https://www.cybo.com/LI-biz/kristina-sprenger-visagistin",
#     "https://www.cybo.com/LI-biz/varga-hair-international-ag",
#     "https://www.cybo.com/LI-biz/mrs-corinna-chesi-coiffeursalon",
#     "https://www.cybo.com/LI-biz/viva-balance",
#     "https://www.cybo.com/LI-biz/salon-brigitte",
#     "https://www.cybo.com/LI-biz/coiffeur-emozioni",
# ]

def safe_find_element(driver, by, value, timeout=5, condition=EC.presence_of_element_located):
    """Safely find an element with an explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(condition((by, value)))
    except Exception:
        return None


def extract_opening_time(driver, day_label):
    """Extracts opening time for a given day."""
    try:
        day_elem = safe_find_element(driver, By.XPATH, f'//div[contains(@class, "weekday-drop")]/div/b[contains(text(), "{day_label}")]/..', timeout=5)
        if not day_elem:
            return "N/A"
        time_elements = day_elem.find_elements(By.XPATH, './/span[@class="hrblk"]/time')
        if len(time_elements) == 2:
            open_time = time_elements[0].get_attribute('datetime').strip()
            close_time = time_elements[1].get_attribute('datetime').strip()
            return f"{open_time} - {close_time}"
        return "Closed" if "Closed" in day_elem.text else "N/A"
    except Exception:
        return "N/A"


def scrape_individual_page(driver):
    """Scrapes data from an individual page."""
    salon_data = {"Name": "N/A", "Address": "N/A", "Phone": "N/A", "Email": "N/A", "Categories": "N/A", "Opening Times": "N/A"}
    try:
        salon_data["Name"] = safe_find_element(driver, By.XPATH, '//h1[@class="top-bname"]/span').text.strip() if safe_find_element(driver, By.XPATH, '//h1[@class="top-bname"]/span') else "N/A"
        salon_data["Address"] = safe_find_element(driver, By.XPATH, '//div[@style="margin: 8px 0px; text-transform: capitalize;"]').text.strip() if safe_find_element(driver, By.XPATH, '//div[@style="margin: 8px 0px; text-transform: capitalize;"]') else "N/A"
        phone_elem = safe_find_element(driver, By.XPATH, '//span[@class="bot-d htc-link hidden-mob"]/a')
        salon_data["Phone"] = phone_elem.text.strip() if phone_elem else "N/A"
        email_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "mailto:")]/span')
        salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"
        category_elems = driver.find_elements(By.XPATH, '//span[@class="sorted_cat"]')
        salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        salon_data["Opening Times"] = {day: extract_opening_time(driver, day) for day in days_of_week}
    except Exception as e:
        print(f"Error scraping page: {e}")
    return salon_data


SALON_URLS = [
    "https://www.cybo.com/LI-biz/coiffeursalon-darte",
    "https://www.cybo.com/LI-biz/coiffeursalon-m-gaube",
    "https://www.cybo.com/LI-biz/coiffeursalon-fris%C3%B6r",
    "https://www.cybo.com/LI-biz/coiffure-zur-schmiede",
    "https://www.cybo.com/LI-biz/salon-liz",
    "https://www.cybo.com/LI-biz/erikas-fusspflegepraxis",
    "https://www.cybo.com/LI-biz/designerama-hair-sabrina-malin",
    "https://www.cybo.com/LI-biz/pakos-barbershop",
    "https://www.cybo.com/LI-biz/haarzentrum",
    "https://www.cybo.com/LI-biz/coiffeur-zur-schmiede",
    "https://www.cybo.com/LI-biz/coiffeur-magic_10",
    "https://www.cybo.com/LI-biz/ruths-scherenzauber",
    "https://www.cybo.com/LI-biz/skinminded-laser-clinics",
    "https://www.cybo.com/LI-biz/haarfrei-jetzt",
    "https://www.cybo.com/LI-biz/birgit",
    "https://www.cybo.com/LI-biz/hair-and-body",
    "https://www.cybo.com/LI-biz/coiffeur-andrea",
    "https://www.cybo.com/LI-biz/mrs-gerda-elkuch-fusspflegesalon_1R",
    "https://www.cybo.com/LI-biz/adventure-coiffeur-manuela",
    "https://www.cybo.com/LI-biz/corina",
    "https://www.cybo.com/LI-biz/haarzentrum-lett_1b",
    "https://www.cybo.com/LI-biz/kristina-sprenger-visagistin",
    "https://www.cybo.com/LI-biz/varga-hair-international-ag",
    "https://www.cybo.com/LI-biz/mrs-corinna-chesi-coiffeursalon",
    "https://www.cybo.com/LI-biz/viva-balance",
    "https://www.cybo.com/LI-biz/salon-brigitte",
    "https://www.cybo.com/LI-biz/coiffeur-emozioni",
]

for idx, url in enumerate(SALON_URLS):
    print(f"\nScraping {idx + 1}/{len(SALON_URLS)}: {url}")
    driver = None
    salon_data = {}

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.set_page_load_timeout(30)

        driver.get(url)

        try:
            consent_button = safe_find_element(driver, By.XPATH, '//button[contains(@class, "fc-cta-consent")]', 5, EC.element_to_be_clickable)
            if consent_button:
                consent_button.click()
                print("Consent button clicked successfully.")
        except Exception as e:
            print("No consent modal detected. Continuing...")

        salon_data = scrape_individual_page(driver)
        salon_data["URL"] = url  

    except KeyboardInterrupt:
        print("\n[INFO] User interrupted the script (Ctrl+C). Closing browser tab...")

    except TimeoutException as e:
        print(f"Timeout for URL: {url}")
        salon_data = {"URL": url, "Error": str(e)}

    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        salon_data = {"URL": url, "Error": str(e)}

    finally:
        if driver:
            try:
                driver.quit()
                print("Browser tab closed successfully.")
            except Exception as e:
                print(f"Error closing the driver: {e}")

    output_filename = f"salon_{idx + 1}.json"
    try:
        with open(output_filename, "w") as json_file:
            json.dump(salon_data, json_file, indent=4)
        print(f"Data saved to {output_filename}.")
    except Exception as e:
        print(f"Error saving file {output_filename}: {e}")

    try:
        input("\nPress Enter to continue to the next URL...")
    except KeyboardInterrupt:
        print("\n[INFO] User interrupted during input. Exiting the script.")
        break

