'''
This script is used to download files from a Google Drive folder.
the script uses the requests library to send an HTTP GET request to the Google Drive URL and downloads the file content.

For now, this script is in testing phase. Can be impleted directly into main.py after testing is done.
'''

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from time import sleep


# options = Options()
# url = 'https://drive.google.com/drive/folders/11_BFC7oH-gG69CfBrJvir6TkRV-5JXLc?usp=sharing'
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# page = driver.get(url)
# sleep(10)
# if page:
#     print("got it")
# else:
#     print("sorry can not go with this method")
# https://drive.google.com/drive/folders/11_BFC7oH-gG69CfBrJvir6TkRV-5JXLc?usp=sharing

import requests as rq

url = 'https://drive.google.com/uc?export=download&confirm=yes&id=11_BFC7oH-gG69CfBrJvir6TkRV-5JXLc'

download_page = rq.get(url)

with open('new.pdf','wb') as new:
    new.write(download_page.content)
    
print("all tasks done successfully")