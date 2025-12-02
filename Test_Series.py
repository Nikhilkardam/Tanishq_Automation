from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import random, time, os

# -----------------------------------------
# CONFIG
# -----------------------------------------
MOBILE_NUMBER = "7838284765"
DEFAULT_OTP = "483217"
URL = "https://prep360.videocrypt.in/"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.maximize_window()


# =========================================================
# ================  HUMAN-LIKE FUNCTIONS  =================
# =========================================================

def human_pause(min_s=0.3, max_s=1.2):
    time.sleep(random.uniform(min_s, max_s))

def human_scroll():
    amt = random.choice([120, 200, 300, 400])
    driver.execute_script(f"window.scrollBy(0, {amt});")
    human_pause()

def human_type(element, text):
    for c in text:
        element.send_keys(c)
        time.sleep(random.uniform(0.05, 0.15))

def human_click(element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    except:
        pass
    human_pause()
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
    human_pause()


# =========================================================
# SAFE SEND KEYS
# =========================================================
def safe_type(locator, text):
    for char in text:
        typed = False
        while not typed:
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                element.send_keys(char)
                typed = True
            except StaleElementReferenceException:
                time.sleep(0.2)


# =========================================================
# POPUP CLOSE
# =========================================================
def close_popup_if_exists():
    try:
        btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.custom-close-button"))
        )
        human_click(btn)
    except:
        pass


# =========================================================
# CHECK LOGIN
# =========================================================
def is_user_logged_in():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login/Register']")))
        return False
    except TimeoutException:
        return True


# =========================================================
# LOGIN FUNCTION
# =========================================================
def perform_login():
    print(">>> Logging in")

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login/Register']")))
    human_click(login_btn)

    mobile_locator = (By.ID, "mobile")
    wait.until(EC.visibility_of_element_located(mobile_locator))
    driver.find_element(*mobile_locator).send_keys(MOBILE_NUMBER)
    human_pause()

    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]")))
    human_click(continue_btn)

    for idx, digit in enumerate(DEFAULT_OTP, start=1):
        otp_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input[aria-label='Please enter OTP character {idx}']")
        ))
        otp_box.send_keys(digit)
        time.sleep(0.15)

    verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Verify')]")))
    human_click(verify_btn)

    human_pause()
    close_popup_if_exists()
    print(">>> Login successful")


# =========================================================
# CLICK LOGO
# =========================================================
def click_logo():
    locators = [
        (By.CSS_SELECTOR, "img.logoImg"),
        (By.XPATH, "//img[@class='logoImg']"),
        (By.XPATH, "//img[contains(@src, 'clientlogo')]")
    ]
    for locator in locators:
        try:
            logo = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            human_click(logo)
            print("✓ Clicked logo")
            return
        except:
            continue
    print("❌ Logo not found")


# =========================================================
# PARTIAL BUTTON LOCATOR (Dynamic)
# =========================================================
def get_button_by_partial(keyword):
    keyword = keyword.lower()
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if keyword in b.text.strip().lower():
            return b
    return None


# =========================================================
# MAIN START
# =========================================================
driver.get(URL)
time.sleep(3)

if not is_user_logged_in():
    perform_login()

click_logo()


# =========================================================
# CLICK LIVE TEST
# =========================================================
human_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Live Test')]"))))
human_pause()


# =========================================================
# LOAD ALL TESTS
# =========================================================
driver.execute_script("window.scrollTo(0, 0);"); human_pause()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"); human_pause()
driver.execute_script("window.scrollTo(0, 0);"); human_pause()


# =========================================================
# CLICK FIRST "Attempt Now"
# =========================================================
buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[normalize-space()='Attempt Now']")))
for btn in buttons:
    if btn.is_displayed() and btn.is_enabled():
        human_click(btn)
        break

# Start Test
human_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))))
human_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Ready To proceed']"))))


# =========================================================
# MAIN HUMAN-LIKE QUESTION LOOP
# =========================================================
question_counter = 0

while True:
    question_counter += 1
    human_pause()

    # Scroll like a human
    human_scroll()

    # get options dynamically
    options = driver.find_elements(By.XPATH, "//label[contains(@for,'option') or contains(@class,'option')]")
    if not options:
        options = driver.find_elements(By.XPATH, "//input[@type='radio']")

    if options:
        random_opt = random.choice(options)
        human_click(random_opt)
        print(f"Answered Q{question_counter}")

    if question_counter % 3 == 0:
        review_btn = get_button_by_partial("review")
        if review_btn:
            human_click(review_btn)

    human_pause()

    next_btn = get_button_by_partial("next")
    if not next_btn or not next_btn.is_enabled():
        break

    human_click(next_btn)
    print(f"Next → Q{question_counter+1}")


# =========================================================
# CLICK SUBMIT
# =========================================================
submit_btn = get_button_by_partial("submit")
if submit_btn:
    human_click(submit_btn)
    human_pause()

# =========================================================
# POPUP SUBMIT BUTTON
# =========================================================
try:
    popup_submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-button.button-submit"))
    )
    human_click(popup_submit)
    print("Popup Submit clicked.")
except:
    print("Popup Submit not found.")



# =========================================================
# WAIT FOR RESULT TABLE BEFORE SCREENSHOT
# =========================================================
try:
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//table | //div[contains(text(), 'Submit Your Test')]")
        )
    )
    human_pause(1.5, 2.5)
except:
    human_pause(2, 3)

# =========================================================
# TAKE FINAL SCREENSHOT (NORMAL DOWNLOADS FOLDER)
# =========================================================

downloads_path = f"C:/Users/{os.getlogin()}/Downloads/test_result_{int(time.time())}.png"

driver.save_screenshot(downloads_path)
print(f"Screenshot saved at: {downloads_path}")


# =========================================================
# PAUSE + RESUME (Future use)
# =========================================================
# def pause_test():
#     btn = get_button_by_partial("pause")
#     if btn:
#         human_click(btn)
#         print("Paused test")

# def resume_test():
#     btn = get_button_by_partial("resume") or get_button_by_partial("continue")
#     if btn:
#         human_click(btn)
#         print("Resumed test")


time.sleep(10)
