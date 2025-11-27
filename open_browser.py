import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------- ANTI-DETECTION OPTIONS ----------------------
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


# ---------------------- HUMAN-LIKE FUNCTIONS ------------------------
def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.25))  # human typing


def human_scroll():
    for _ in range(random.randint(2, 4)):
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(random.uniform(0.3, 0.8))


def human_mouse_move():
    actions.move_by_offset(random.randint(20, 80), random.randint(20, 80)).perform()
    time.sleep(random.uniform(0.3, 0.8))


def human_pause():
    time.sleep(random.uniform(1, 2))


# ---------------------- STEP 1: OPEN DUCKDUCKGO ----------------------
driver.get("https://duckduckgo.com/")
human_pause()
human_mouse_move()

# ---------------------- STEP 2: SEARCH FOR GOOGLE ----------------------
search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
human_type(search_box, "https://www.google.com/")
search_box.send_keys(Keys.ENTER)
human_scroll()
human_mouse_move()

print(driver.title)
print(driver.current_url)
# print(driver.page_source)

# ---------------------- STEP 3: CLICK GOOGLE RESULT ----------------------
google_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "google.com")))
google_link.click()
human_pause()
human_mouse_move()

# ---------------------- STEP 4: ON GOOGLE, SEARCH YOUTUBE ----------------------
google_search = wait.until(EC.presence_of_element_located((By.NAME, "q")))
human_type(google_search, "https://www.youtube.com/")
google_search.send_keys(Keys.ENTER)

human_scroll()
human_mouse_move()

# ---------------------- PRINT INFO ----------------------
print(driver.title)
print(driver.current_url)
# print(driver.page_source)
# ---------------------- STEP 5: NAVIGATIONS ----------------------
driver.back()
human_pause()

driver.forward()
human_pause()

driver.refresh()
human_pause()

# print("After navigation:")
# print(driver.title)
# print(driver.current_url)

time.sleep(5)
driver.quit()
