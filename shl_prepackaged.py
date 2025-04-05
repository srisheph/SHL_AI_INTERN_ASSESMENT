
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import undetected_chromedriver as uc
import time

# Start Chrome driver
driver = uc.Chrome()
driver.get("https://www.shl.com/solutions/products/product-catalog/?type=2")

data = []

while True:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 4:
            continue

        test_name = cols[0].text.strip()
        link = cols[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        remote_testing = "Yes" if "●" in cols[1].text else "No"
        adaptive_irt = "Yes" if "●" in cols[2].text else "No"
        test_type = " ".join(cols[3].text.strip().split("\n"))

        data.append([test_name, remote_testing, adaptive_irt, test_type, link])

    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(text(),'Next') and contains(@href,'type=2')]")
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(2)
    except:
        break

df = pd.DataFrame(data, columns=["Test Name", "Remote Testing", "Adaptive/IRT", "Test Type", "Link"])
df.to_csv("shl_part1.csv", index=False, encoding="utf-8")

driver.quit()
print("✅ Part 1 scraping done!")

