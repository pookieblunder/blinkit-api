from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time

# =========================
# CONFIG
# =========================
BASE_URL = "https://blinkit.com"
CATEGORIES_URL = "https://blinkit.com/categories"

# =========================
# MONGO SETUP
# =========================
client = MongoClient('localhost', 27017)
db = client['blinkit']
url_collection = db['url']  # your collection

# =========================
# SELENIUM SETUP
# =========================
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--headless")  # headless mode if you want

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# =========================
# OPEN PAGE
# =========================
driver.get(CATEGORIES_URL)
time.sleep(5)  # wait for JS to fully load

# =========================
# SCRAPE SECTIONS AND SUBCATEGORIES
# =========================
sections = driver.find_elements(By.TAG_NAME, "h2")
print(f"🔍 Found {len(sections)} sections")

for h2 in sections:
    section_name = h2.text.strip()
    # Get the next sibling <div> that contains subcategories
    div = h2.find_element(By.XPATH, "following-sibling::div[1]")
    subcategories = div.find_elements(By.TAG_NAME, "a")

    for sub in subcategories:
        name = sub.text.strip()
        url = sub.get_attribute("href")

        if not name or not url:
            continue

        doc = {
            "section": section_name,
            "name": name,
            "url": url,
            "status": "pending"
        }

        # Insert into MongoDB, avoid duplicates
        try:
            url_collection.update_one(
                {"url": url},
                {"$setOnInsert": doc},
                upsert=True
            )
            print(f"✅ Saved: {section_name} -> {name}")
        except Exception as e:
            print(f"❌ Failed: {name} | {e}")

# =========================
# CLEANUP
# =========================
driver.quit()
client.close()
print("🎉 All subcategory links saved with correct section info!")
