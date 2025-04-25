import os
import time
import uuid
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

# Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment if you want to run without opening a window
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
service = Service("../chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL with pre-applied filters
base_url = (
    "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/"
    "kujawsko--pomorskie/bydgoszcz/bydgoszcz/bydgoszcz"
    "?limit=72&ownerTypeSingleSelect=ALL&areaMin=35&areaMax=60"
    "&buildYearMin=2010&extras=%5BLIFT%5D&by=LATEST&direction=DESC"
    "&viewType=listing"
)
driver.get(base_url)

# Accept cookies if needed
try:
    accept_cookies = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    accept_cookies.click()
    print("✅ Cookies accepted.")
except TimeoutException:
    pass

# Wait for listings to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-cy='listing-item']"))
    )
except TimeoutException:
    print("❌ Timeout: Listings did not load.")
    driver.quit()
    exit()

# Scraping setup
all_offers = []
page = 1
max_pages = 3 #only for testing purposes CHANGE LATER

while page <= max_pages:
    print(f"🔍 Scraping - page {page}...")

    # Scroll to 90% page height -> otherwise unable to switch pages
    total_height = driver.execute_script("return document.body.scrollHeight")
    target_height = int(total_height * 0.9)
    current_height = 0
    step = int(total_height * 0.05) or 500

    while current_height < target_height:
        driver.execute_script(f"window.scrollBy(0, {step});")
        current_height += step
        time.sleep(1)
    time.sleep(2)

    # Collect listings
    listings = driver.find_elements(By.CSS_SELECTOR, "article[data-cy='listing-item']")
    if not listings:
        print("⚠️ No listings found on this page.")
        break

    for listing in listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, "p[data-cy='listing-item-title']").text
        except (NoSuchElementException, StaleElementReferenceException):
            title = None

        try:
            price = listing.find_element(By.CSS_SELECTOR, "span[data-sentry-component='Price']").text
        except (NoSuchElementException, StaleElementReferenceException):
            price = None

        try:
            location = listing.find_element(By.CSS_SELECTOR, "p[data-sentry-component='Address']").text
        except (NoSuchElementException, StaleElementReferenceException):
            location = None

        area = rooms = None
        try:
            description_list = listing.find_elements(By.CSS_SELECTOR, "dl[data-sentry-element='DescriptionList'] dt")
            for dt in description_list:
                label = dt.text.strip()
                try:
                    value = dt.find_element(By.XPATH, "following-sibling::dd[1]").text.strip()
                except NoSuchElementException:
                    value = None

                if label == "Powierzchnia":
                    area = value
                elif label == "Liczba pokoi":
                    rooms = value
        except (NoSuchElementException, StaleElementReferenceException):
            pass

        try:
            url = listing.find_element(By.CSS_SELECTOR, "a[data-cy='listing-item-link']").get_attribute("href")
        except (NoSuchElementException, StaleElementReferenceException):
            url = None

        all_offers.append({
            "title": title,
            "price": price,
            "area": area,
            "rooms": rooms,
            "location": location,
            "url": url
        })

    # Move to the next page
    try:
        current_page_element = driver.find_element(By.CSS_SELECTOR, "ul[data-cy*='pagination'] li[aria-selected='true']")
        next_page_element = current_page_element.find_element(By.XPATH, "following-sibling::li[1][@aria-disabled='false']")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_page_element)
        time.sleep(1)
        next_page_element.click()
        page += 1
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-cy='listing-item']"))
        )
    except (NoSuchElementException, TimeoutException):
        print("✔️ No more pages. Scraping finished.")
        break

# Save results to Excel
# Save results to Excel
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # go one level up from src/
exports_dir = os.path.join(root_dir, "excel_exports")

if not os.path.exists(exports_dir):
    os.makedirs(exports_dir)

df = pd.DataFrame(all_offers)
if df.empty:
    print("⚠️ No offers collected. No file was saved.")
else:
    filename = f"otodom_offers_{uuid.uuid4().hex[:8]}.xlsx"
    path = os.path.join(exports_dir, filename)
    df.to_excel(path, index=False)
    print(f"📄 File saved: {path}")

# Close browser
driver.quit()
