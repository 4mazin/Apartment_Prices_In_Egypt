from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import os

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

for page in range(2000, 2500):
    if page == 1:
        url = "https://www.bayut.eg/en/egypt/apartments-for-sale/"
    else:
        url = f"https://www.bayut.eg/en/egypt/apartments-for-sale/page-{page}/"

    driver.get(url)
    page_data = extract_apartments()
    all_apartments.extend(page_data)

# Create DataFrame from your new scrape
df_new = pd.DataFrame(all_apartments)

file_name = "bayut_apartments.xlsx"

if os.path.exists(file_name):
    # Load existing Excel file
    df_existing = pd.read_excel(file_name)

    # Append new data
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_combined = df_new

# Save back to Excel
df_combined.to_excel(file_name, index=False)



