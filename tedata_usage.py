import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


DOMAIN = "https://my.te.eg"
SERVICE_NUMBER = sys.argv[1] if len(sys.argv) >= 2 else os.getenv("TEDATA_SERVICE_NUMBER")
SERVICE_PASSWORD = sys.argv[2] if len(sys.argv) >= 3 else os.getenv("TEDATA_SERVICE_PASSWORD")

if not SERVICE_NUMBER or not SERVICE_PASSWORD:
    print("tedata_usage: service number and password are required")
    sys.exit(1)

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 2)
    driver.get(f"{DOMAIN}/#/home/signin")
    driver.find_element_by_id("MobileNumberID").send_keys(SERVICE_NUMBER)
    driver.find_element_by_id("PasswordID").send_keys(SERVICE_PASSWORD+Keys.RETURN)
    #driver.find_element_by_id("singInBtn").click()
    result = wait.until(presence_of_element_located((By.CSS_SELECTOR, ".adsl_usage_prepaid circle-progress>svg>text")))
    usage = result.text.strip().split(" ")[0]
    print(f"{usage} GB")
