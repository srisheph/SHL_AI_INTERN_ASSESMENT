from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import undetected_chromedriver as uc
import time

driver = uc.Chrome()
driver.get("https://www.shl.com/solutions/products/product-catalog/")

data = []

for page in range(0, 32):  # 32 pages in second table
    url = f"https://www.shl.com/solutions/products/product-catalog/?start={page * 12}"
    driver.get(url)
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

    tables = driver.find_elements(By.TAG_NAME, "table")
    if len(tables) < 2:
        print(f"Skipping page {page+1}, second table not found")
        continue

    table = tables[1]
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 4:
            continue

        # Get test name and link from <a> inside first column
        try:
            link_element = cols[0].find_element(By.TAG_NAME, "a")
            test_name = link_element.text.strip()
            test_link = link_element.get_attribute("href")
        except:
            test_name = cols[0].text.strip()
            test_link = ""

        remote_testing = "Yes" if "●" in cols[1].text else "No"
        adaptive_irt = "Yes" if "●" in cols[2].text else "No"
        test_type = " ".join(cols[3].text.strip().split("\n"))

        data.append([test_name, remote_testing, adaptive_irt, test_type, test_link])

df = pd.DataFrame(data, columns=["Test Name", "Remote Testing", "Adaptive/IRT", "Test Type", "Link"])
df.to_csv("shl_main_catalog.csv", index=False, encoding="utf-8")

driver.quit()
print("✅ Main Catalog (with links) saved as 'shl_main_catalog.csv'")
