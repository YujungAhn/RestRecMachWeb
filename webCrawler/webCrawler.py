from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def naverMapCrawler() :
    chromedriver = 'C:/chromedriver_win32/chromedriver'
    driver = webdriver.Chrome(chromedriver)

    naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query=등촌동%20이디야&sm=hty&style=v5"
    driver.get(naver_map_search_url)

    test = driver.find_element(By.CSS_SELECTOR, "#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
    print(test)

    # 상세 페이지
    # https://m.place.naver.com/restaurant/