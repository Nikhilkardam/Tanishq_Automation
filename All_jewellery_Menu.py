from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://duckduckgo.com/")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("tanishq", Keys.ENTER)

# ---- Scroll to load results ----
for i in range(3):
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

# ---- Click Tanishq result ----
tanishq_link = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Tanishq')]"))
)
tanishq_link.click()

print("Opened Tanishq page")
time.sleep(4)

# -------- FIX: reset scroll (THIS SOLVES THE ERROR) --------
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(1)

# ---- Hover over JEWELLERY menu ----
jewellery_menu = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.ID, "tq-jewellery"))
)

ActionChains(driver).move_to_element(jewellery_menu).perform()
time.sleep(1.5)

# ---- Now click “All Jewellery” ----
all_jewellery = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "All Jew"))
)

all_jewellery.click()

print("Opened All Jewellery section")

time.sleep(3)
print("Hi Nikhil, code successfully executed")
driver.quit()
