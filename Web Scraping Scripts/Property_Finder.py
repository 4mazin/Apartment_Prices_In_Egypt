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

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'li[data-testid^="list-item-"]')
        )
    )

    cards = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid^="list-item-"]')
    
    for card in cards:

        try:
            type = card.find_element(By.CLASS_NAME, "styles-module_content__property-type__qxCMa").text
        except:
            type = None

        try:
            location = card.find_element(By.CLASS_NAME, "styles-module_content__location__yBL3r").text
        except:
            location = None
        
        try:
            details = card.find_elements(
                By.CSS_SELECTOR,
                "div.styles-module_content__details__2Nndo p"
            )

            number_of_bedrooms = None
            number_of_bathrooms = None
            area = None

            numeric_values = []

            for item in details:
                text = item.text.strip()

                # Area contains sqm or m²
                if "sqm" in text.lower():
                    area = text
                else:
                    numeric_values.append(text)

            number_of_bedrooms = numeric_values[0]

            number_of_bathrooms = numeric_values[1]

        except:
            number_of_bedrooms = None
            number_of_bathrooms = None
            area = None
        
        try:
            price = card.find_element(By.CLASS_NAME, "styles-module_content__price__TBYWv").text
        except:
            price=None
        
        apartments.append({
            "Type": type,
            "Location": location,
            "Area": area,
            "Number Of Bedrooms": number_of_bedrooms,
            "Number Of Bathrooms": number_of_bathrooms,
            "Price": price
        })

    return apartments
    
allApartments = []

for page in range(300, 600):
    if page == 1:
        url = "https://www.propertyfinder.eg/en/search?c=1&t=44&fu=0&ob=mr"
    else:
        url = f"https://www.propertyfinder.eg/en/search?c=1&t=44&fu=0&ob=mr&page={page}"
    
    driver.get(url)
    pageData = extract_apartments()
    allApartments.extend(pageData)

df_new = pd.DataFrame(allApartments)

file_name = "propertyFinder_chalet.xlsx"

if os.path.exists(file_name):
    # Load existing Excel file
    df_existing = pd.read_excel(file_name)

    # Append new data
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_combined = df_new

# Save back to Excel
df_combined.to_excel(file_name, index=False)






#<div data-testid="property-card-down-payment-tag" class="tag-module_tag__jFU3w tag-module_tag--rounded__ZYOkW tag-module_tag-size--large__tD7hV styles-module_content__tag--secondary__34Wga">Down payment: 1,400,000 EGP</div>