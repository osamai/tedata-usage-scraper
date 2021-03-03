from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


DOMAIN = "https://my.te.eg"
SERVICE_NUMBER = ""
SERVICE_PASSWORD = ""

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 2)
    driver.get(DOMAIN+"/#/home/signin")
    driver.find_element_by_id("MobileNumberID").send_keys(SERVICE_NUMBER)
    driver.find_element_by_id("PasswordID").send_keys(SERVICE_PASSWORD+Keys.RETURN)
    #driver.find_element_by_id("singInBtn").click()
    result = wait.until(presence_of_element_located((By.CSS_SELECTOR, ".adsl_usage_prepaid circle-progress>svg>text")))
    usage = result.text.strip().split(" ")[0]
    print(f"{usage} GB")
