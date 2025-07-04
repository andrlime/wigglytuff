"""
A Selenium driver factory that produces several parallel Chrome drivers
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def driver_factory():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    # service = Service("")

    return webdriver.Chrome(service=service, options=chrome_options)
