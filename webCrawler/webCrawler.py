from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


chromedriver = 'C:/chromedriver_win32/chromedriver'
driver = webdriver.Chrome(chromedriver)

driver.get("https://sports.news.naver.com/kbaseball/index.nhn")

title = driver.find_element(By.CSS_SELECTOR, "#content > div > div.home_feature > div.feature_side > div").text
print(title)