import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


DOMAIN = "https://my.te.eg"
SERVICE_NUMBER = sys.argv[1] if len(sys.argv) > 1 else os.getenv("TEDATA_NUMBER")
SERVICE_PASSWORD = sys.argv[2] if len(sys.argv) > 2 else os.getenv("TEDATA_PASSWORD")
DEV_MODE = os.getenv("DEV_MODE", "0") == "1"

if not SERVICE_NUMBER or not SERVICE_PASSWORD:
    print("tedata_usage: service number and password are required")
    sys.exit(1)


opts = webdriver.FirefoxOptions()
opts.headless = not DEV_MODE

with webdriver.Firefox(options=opts, service_log_path="/dev/null") as driver:
    driver.get(f"{DOMAIN}/user/login")

    wait = WebDriverWait(driver, 10)

    # login
    wait.until(presence_of_element_located((By.CLASS_NAME, "p-inputmask"))).send_keys(
        SERVICE_NUMBER
    )
    driver.find_element_by_id("password").send_keys(SERVICE_PASSWORD + Keys.RETURN)

    # getting info
    wrapper = wait.until(presence_of_element_located((By.CLASS_NAME, "gauge-carousel")))
    plan = driver.find_element_by_css_selector("h1.text-primary").text.strip()
    subtype = wrapper.find_element_by_class_name("gauge-caption").text.strip()
    remaining = (
        wrapper.find_element_by_class_name("remaining-details")
        .text.strip()
        .split("\n")[0]
    )
    used = (
        wrapper.find_element_by_class_name("usage-details").text.strip().split(" ")[0]
    )

    print(f"Plan:      {plan}")
    print(f"Type:      {subtype}")
    print(f"Used:      {used} GB")
    print(f"Remaining: {remaining} GB")
