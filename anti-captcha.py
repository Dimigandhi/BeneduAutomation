import os, time, json, requests

# from time import gmtime, strftime
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

# Anti-Captcha API URL
API_URL = "https://api.anti-captcha.com/createTask"
# Anti-Captcha API-KEY
API_KEY = "b13a4d5d02334e34c33b02a82c4bfef1"
# Benedu Site Key
site_Key = "6Lcx81EUAAAAAAHX3UAIdQnNSBjnb0XOPcegqOjZ"

# Localhost Site Key
site_Key = "6LfhymQUAAAAAOVG5FQtdIbEcw_ywvv_P841oYMb"

json_req = json.dumps({"clientKey":API_KEY,
                       "task":{"type":"NoCaptchaTaskProxyless",
                               # "websiteURL":"https://www.benedu.co.kr",
                               "websiteURL":"https://localhost",
                               "websiteKey":site_Key},
                       "softId":0,
                       "languagePool":"en"})

results = requests.post(API_URL, data=json_req)
print(results.text)

# driver = webdriver.Chrome('chromedriver.exe')