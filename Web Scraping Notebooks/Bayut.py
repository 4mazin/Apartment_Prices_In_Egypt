from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)


def extract_apartments():
    apartments = []

    cards = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul > li")
    )
)

    for card in cards:
        try:
            location = card.find_element(By.CLASS_NAME, "_51c6b1ca").text
        except:
            location = None

        try:
            details = card.find_elements(By.CSS_SELECTOR, ".c377cd7b._3002c6fb")
            beds = details[1].text if len(details) > 0 else None
            bath_rooms = details[2].text if len(details) > 1 else None
        except:
            beds = None
            bath_rooms = None

        try:
            price = card.find_element(By.CLASS_NAME, "eff033a6").text
        except:
            price = None

        try:
            downPayment = card.find_element(By.CLASS_NAME, "fd7ade6e").text
        except:
            downPayment = None
    
        apartments.append({
            "Location": location,
            "Beds": beds,
            "Bathrooms": bath_rooms,
            "Price": price,
            "Down Payment": downPayment
        })

    return apartments

all_apartments = []

for page in range(1, 2):
    if page == 1:
        url = "https://www.bayut.eg/en/egypt/apartments-for-sale/"
    else:
        url = f"https://www.bayut.eg/en/egypt/apartments-for-sale/page-{page}/"

    driver.get(url)
    time.sleep(3)
    page_data = extract_apartments()
    all_apartments.extend(page_data)

df = pd.DataFrame(all_apartments)
df.to_excel("bayut_apartments.xlsx", index=False)




