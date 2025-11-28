from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time, random

# -----------------------------------------
# CONFIG
# -----------------------------------------
MOBILE_NUMBER = "7838284765"
DEFAULT_OTP = "483217"
URL = "https://prep360.videocrypt.in/"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.maximize_window()
# -----------------------------------------
# SAFE SEND KEYS (Fixes stale element)
# -----------------------------------------
def safe_type(locator, text):
    for char in text:
        typed = False
        while not typed:
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                element.send_keys(char)
                typed = True
            except StaleElementReferenceException:
                print("[!] Stale element, retrying typing...")
                time.sleep(0.2)

# -----------------------------------------
# CLOSE POPUP
# -----------------------------------------
def close_popup_if_exists():
    try:
        btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.custom-close-button"))
        )
        btn.click()
    except:
        pass

# -----------------------------------------
# CHECK LOGIN
# -----------------------------------------
def is_user_logged_in():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login/Register']")))
        return False
    except TimeoutException:
        return True

# -----------------------------------------
# LOGIN FUNCTION (bulletproof)
# -----------------------------------------
def perform_login():
    print(">>> Opening Login Modal")

    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Login/Register']"))
    )
    login_btn.click()

    time.sleep(1)

    print(">>> Entering mobile number")

    # Correct mobile field locator (perfect)
    mobile_locator = (By.ID, "mobile")

    wait.until(EC.visibility_of_element_located(mobile_locator))
    wait.until(EC.element_to_be_clickable(mobile_locator))

    mobile_input = driver.find_element(*mobile_locator)
    mobile_input.clear()
    mobile_input.send_keys(MOBILE_NUMBER)

    time.sleep(0.5)

    print(">>> Clicking Continue button")

    continue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(),'Continue')]"))
    )
    continue_btn.click()

    time.sleep(1.5)

    print(">>> Entering OTP")

    for idx, digit in enumerate(DEFAULT_OTP, start=1):
        otp_box = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                f"input[aria-label='Please enter OTP character {idx}']"
            ))
        )
        otp_box.send_keys(digit)
        time.sleep(0.15)

    print(">>> Clicking Verify button")

    verify_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(),'Verify')]"))
    )
    verify_btn.click()

    time.sleep(2)
    close_popup_if_exists()

    print(">>> Login successful!")




# -----------------------------------------
# CLICK LOGO
# -----------------------------------------
def click_logo():
    print(">>> Waiting for logo...")

    # best & exact locator (fastest)
    locators = [
        (By.CSS_SELECTOR, "img.logoImg"),
        (By.XPATH, "//img[@class='logoImg']"),
        (By.XPATH, "//img[contains(@src, 'clientlogo')]")
    ]

    logo = None

    # Try all locators one by one
    for locator in locators:
        try:
            logo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            break
        except:
            continue

    if not logo:
        print("❌ Could not find logo using any locator!")
        return

    # Scroll + click with fallback
    driver.execute_script("arguments[0].scrollIntoView(true);", logo)
    time.sleep(1)

    try:
        driver.execute_script("arguments[0].click();", logo)
        print("✓ Logo clicked successfully!")
    except:
        print("❌ Failed to click logo")

# -----------------------------------------
# MAIN
# -----------------------------------------
driver.get(URL)
time.sleep(3)

if is_user_logged_in():
    print(">>> User already logged in")
else:
    print(">>> User NOT logged in")
    perform_login()

click_logo()


# ----> CLicking on live test button <---
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Live Test')]"))
).click()
time.sleep(10)