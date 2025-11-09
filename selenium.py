from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

driver = webdriver.Chrome('./chromewebdriver')

driver.get("https://study.gisma.com/courses/16025/users")

print(driver.title)


with open('config.json') as config:
    config_data = json.load(config)