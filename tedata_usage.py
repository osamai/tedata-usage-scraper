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


opts = webdriver.FirefoxOptions()
opts.headless = True

with webdriver.Firefox(options=opts, service_log_path="/dev/null") as driver:
    driver.get(f"{DOMAIN}/#/home/signin")

    wait = WebDriverWait(driver, 10)

    # switch language to english
    wait.until(presence_of_element_located((By.CSS_SELECTOR, "ecare-langswitcher>button"))).click()

    # login
    driver.find_element_by_id("MobileNumberID").send_keys(SERVICE_NUMBER)
    driver.find_element_by_id("PasswordID").send_keys(SERVICE_PASSWORD + Keys.RETURN)

    # getting info
    wrapper = wait.until(presence_of_element_located((By.CSS_SELECTOR, ".adsl_usage_prepaid")))
    subtype = wrapper.find_element_by_class_name("outterTitle").text.strip()
    remaining = wrapper.find_element_by_css_selector("circle-progress>svg>text").text.strip().split(" ")[0]
    info = wrapper.find_element_by_tag_name("p").text.strip().split(" ")

    print(f"Type:      {subtype}")
    print(f"Total:     {info[-2]} GB")
    print(f"Used:      {info[0]} GB")
    print(f"Remaining: {remaining} GB")
