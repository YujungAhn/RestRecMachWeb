from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import numpy as np
import tqdm

from modeling import reviewData

chromedriver = 'C:/chromedriver_win32/chromedriver'
driver = None


def findUrlinKakaoMap(keyword):
    '''
    kakao Map에서 keyword로 검색하여 상세 페이지 주소 찾기
    '''
    kakao_map_search_url = f"https://map.kakao.com/?q={keyword}"
    try:
        driver.get(kakao_map_search_url)
        time.sleep(3.5)
        # 먼저 시도
        result = driver.find_element_by_css_selector(
            "#info\.search\.place\.list > li:nth-child(1) > div.info_item > div.contact.clickArea > a.moreview").get_attribute(
            'href')

        # 재시도
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):  # child(1)이 없던데요?
            try:
                result = driver.find_element_by_css_selector(
                    "#info\.search\.place\.list > li > div.info_item > div.contact.clickArea > a.moreview").get_attribute(
                    'href')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                result = np.nan
                time.sleep(1)
        else:
            pass

    return result


def findReviewInKakaoMapUrl(url) -> reviewData:
    """
    kakao Map에서 keyword로 검색하여 상세 페이지 주소 찾기
    return
    result ={}
    result['blog_review_list']
    result['kakao_map_name_list']
    result['blog_review_qty_list']
    result['kakao_map_star_review_stars_list']
    result['kakao_map_star_review_qty_list']
    """
    driver.get(url)
    time.sleep(1)
    review_text = ""
    result = {}

    try:
        kakao_map_name = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2").text
        blog_review_qty = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(5) > span").text
        star_review_stars = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b.inactive").text
        star_review_qty = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g").text
    except Exception as e1:
        if "inactive" in str(e1):
            star_review_stars = driver.find_element_by_css_selector(
                "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b").text
            star_review_qty = driver.find_element_by_css_selector(
                "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g").text
        else:
            print(f"\'{url}\' 데이터의 평점 갯수 크롤링에 다른 문제가 생겼다")

    num = 0
    try:
        while num < 3:
            try:
                num += 1
                review_text = review_text + driver.find_element_by_css_selector(
                    f"div.wrap_list > ul > li:nth-child({num}) > a > div.review_story > p").text

                if num == 3:
                    reviewData.review_text = review_text  # 3개나 찾았으면 그만 찾고 나감
                    reviewData.kakao_map_name = kakao_map_name
                    reviewData.blog_review_qty = blog_review_qty
                    reviewData.star_review_stars = star_review_stars
                    reviewData.star_review_qty = star_review_qty
                    break
            except Exception as e1:
                if "li:nth-child(1)" in str(e1):  # child(1)이 없던데요? -> 리뷰가 하나도 없는 것
                    print(f"문제가 발생 - 리뷰가 없음")
                    review_text = "empty"
                    reviewData.review_text = review_text
                    reviewData.kakao_map_name = kakao_map_name
                    reviewData.blog_review_qty = blog_review_qty
                    reviewData.star_review_stars = star_review_stars
                    reviewData.star_review_qty = star_review_qty
                    break
                else:
                    print(f"문제가 발생 - 리뷰가 {num - 1}개뿐이다")
                    reviewData.review_text = review_text  # 일단 리뷰가 하나도 없는 건 아니니 붙이고 탈출 / 리뷰 딸랑 하나 있으면 발생할 수 있음
                    reviewData.kakao_map_name = kakao_map_name
                    reviewData.blog_review_qty = blog_review_qty
                    reviewData.star_review_stars = star_review_stars
                    reviewData.star_review_qty = star_review_qty
                    break

    except Exception as e2:
        print(e2)
        print(f"문제 발생 - code 2")
    return result


def initDriver():
    global driver
    driver = webdriver.Chrome(chromedriver)


def quitDriver():
    try:
        driver.quit()
    except Exception as e:
        print(e)


# !네이버 맵으로 변경 필요
def naverMapCrawler():
    naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query=등촌동%20이디야&sm=hty&style=v5"
    driver.get(naver_map_search_url)

    test = driver.find_element(By.CSS_SELECTOR,
                               "#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute(
        'data-cid')
    print(test)

    # 상세 페이지
    # https://m.place.naver.com/restaurant/
