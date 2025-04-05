from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Load your existing CSV file
df = pd.read_csv("combined.csv")

# Initialize WebDriver (headless mode to avoid browser popup)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to extract duration from the test page
def get_duration(url):
    try:
        driver.get(url)
        time.sleep(2)  # wait for page to load
        # Try common location for duration text
        duration_element = driver.find_element(By.XPATH, "//p[contains(text(),'minute')]")
        return duration_element.text
    except Exception as e:
        print(f"❌ Duration not found for {url}")
        return "Unknown"

# Apply for each row
durations = []
for index, row in df.iterrows():
    print(f"⏳ Processing ({index + 1}/{len(df)}): {row['Test Name']}")
    durations.append(get_duration(row['Link']))

# Add to DataFrame
df['Duration'] = durations

# Save updated CSV
df.to_csv("shl_tests_with_duration.csv", index=False)
print("✅ Done! File saved as shl_tests_with_duration.csv")

# Close driver
driver.quit()
