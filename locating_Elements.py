from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v140.debugger import search_in_content
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.duckduckgo.com/")
search_box = driver.find_element(By.NAME, "q")
search_box.click()
search_box.send_keys("tanishq")
search_box.send_keys(Keys.ENTER)

# ---> Scroll on page <---

for i in range(5):
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(1)
# ----> clicking on the main link >-----

driver.find_element(By.LINK_TEXT, "Tanishq - Shop the best gold and diamond jewellery designs from India's ...").click()


# ----- Your code here -----
# search= driver.find_element()
time.sleep(3)
print("Hi Nikhil this code is successfully executed")
driver.quit()