import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# List of URLs
SALON_URLS = [
    "https://www.cybo.com/LI-biz/fusspflege-in-mauren-martina-b%C3%BCchel",
    "https://www.cybo.com/LI-biz/coiffeur-klaudia",
    "https://www.cybo.com/LI-biz/salon-mano-anstalt",
    "https://www.cybo.com/LI-biz/sie-er-coiffure",
    "https://www.cybo.com/LI-biz/coiffeursalon-studio-haarscharf",
    "https://www.cybo.com/LI-biz/estilo-libre-hair-beauty",
    "https://www.cybo.com/LI-biz/tona-hairstyle",
    "https://www.cybo.com/LI-biz/salon-niedhart-damen-und-herren",
    "https://www.cybo.com/LI-biz/salon-astrid",
    "https://www.cybo.com/LI-biz/studio-haar-kult-mauren",
    "https://www.cybo.com/LI-biz/coiffeur-les-artistes",
    "https://www.cybo.com/LI-biz/coiffure-fabrizio",
    "https://www.cybo.com/LI-biz/gidor-coiffure-vaduz",
    "https://www.cybo.com/LI-biz/a-kerhart-coiffeur-headroom_1C",
    "https://www.cybo.com/LI-biz/haarlocke-frisuren-mehr",
    "https://www.cybo.com/LI-biz/top-hair",
    "https://www.cybo.com/LI-biz/secrets-of-beauty-est",
    "https://www.cybo.com/LI-biz/big-coiffeur",
    "https://www.cybo.com/LI-biz/coiffeursalon-herrensalon-vincenzo",
    "https://www.cybo.com/LI-biz/a-kerhart-coiffeur-headroom",
    "https://www.cybo.com/LI-biz/h%C3%A4%C3%A4r-%C3%A4nd-sch%C3%A4r",
    "https://www.cybo.com/LI-biz/coiffeursalon-em",
    "https://www.cybo.com/LI-biz/mrs-beatrice-w%C3%BCst-fusspflegesalon",
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

def safe_find_element(driver, by, value, timeout=10, condition=EC.presence_of_element_located):
    """Safely find element with explicit wait."""
    try:
        return WebDriverWait(driver, timeout).until(
            condition((by, value))
        )
    except Exception:
        return None

def extract_opening_time(driver, day_label):
    """Extracts opening time for a given day."""
    try:
        day_elem = safe_find_element(driver, By.XPATH, f'//div[contains(@class, "weekday-drop")]/div/b[contains(text(), "{day_label}")]/..', timeout=10)
        if day_elem:
            closed_elem = day_elem.find_elements(By.XPATH, './/span[@class="hrblk"]')
            if closed_elem and "Closed" in closed_elem[0].text:
                return "Closed"
            time_elements = day_elem.find_elements(By.XPATH, './/span[@class="hrblk"]/time')
            if len(time_elements) == 2:
                open_time = time_elements[0].get_attribute('datetime').strip()
                close_time = time_elements[1].get_attribute('datetime').strip()
                return f"{open_time} - {close_time}"
        return "N/A"
    except Exception:
        return "N/A"

def scrape_individual_page(driver):
    """Scrapes data from an individual page."""
    salon_data = {}
    try:
        # Extract Name
        name_elem = safe_find_element(driver, By.XPATH, '//h1[@class="top-bname"]/span')
        salon_data["Name"] = name_elem.text.strip() if name_elem else "N/A"

        # Extract Address
        address_elem = safe_find_element(driver, By.XPATH, '//div[@style="margin: 8px 0px; text-transform: capitalize;"]')
        salon_data["Address"] = address_elem.text.strip() if address_elem else "N/A"

        # Extract Phone
        phone_elem = safe_find_element(driver, By.XPATH, '//span[@class="bot-d htc-link hidden-mob"]/a')
        raw_phone = phone_elem.text.strip() if phone_elem else "N/A"
        salon_data["Phone"] = f"+423 {raw_phone}" if raw_phone != "N/A" else "N/A"

        # Extract Email
        email_elem = safe_find_element(driver, By.XPATH, '//a[starts-with(@href, "mailto:")]/span')
        salon_data["Email"] = email_elem.text.strip() if email_elem else "N/A"

        # Extract Categories
        category_elems = driver.find_elements(By.XPATH, '//span[@class="sorted_cat"]')
        salon_data["Categories"] = [elem.text.strip() for elem in category_elems if elem.text.strip()]

        # Extract Opening Times
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        opening_times = {day: extract_opening_time(driver, day) for day in days_of_week}
        salon_data["Opening Times"] = opening_times

    except Exception as e:
        print(f"Error scraping individual page: {e}")
    return salon_data

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# List to store all salons' data
all_salons_data = []

# Iterate through each salon URL
for idx, url in enumerate(SALON_URLS):
    print(f"Scraping {idx + 1}/{len(SALON_URLS)}: {url}")
    try:
        driver.get(url)

        # Handle Consent Modal if it appears
        try:
            consent_button = safe_find_element(driver, By.XPATH, '//button[contains(@class, "fc-cta-consent")]', timeout=5, condition=EC.element_to_be_clickable)
            if consent_button:
                consent_button.click()
                print("Consent button clicked successfully.")
        except Exception as e:
            print("No consent modal detected. Continuing...")

        # Scrape data from the current page
        salon_data = scrape_individual_page(driver)
        all_salons_data.append(salon_data)

    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        all_salons_data.append({"URL": url, "Error": str(e)})

# Quit WebDriver
driver.quit()

# Save all scraped data to a single JSON file
output_filename = "all_salons_data.json"
with open(output_filename, "w") as json_file:
    json.dump(all_salons_data, json_file, indent=4)
print(f"Data saved to {output_filename}.")
