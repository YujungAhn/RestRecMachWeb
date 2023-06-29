import logging

from tqdm import tqdm_notebook

import publicData.publicData as publicData
from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도
import webCrawler
import numpy as np


def recommandRes(name, areaCd, resCount):
    """
    상권 데이터, 리뷰데이터를 활용해 유사도가 높은 식당을 추천
    name : 식당 이름
    areaCd : 식당의 지역 코드
    resCount :
    """
    # 동별 상권정보 정보 조회
    df = publicData.getAllStoreListInDong(areaCd)

    # 음식점 데이터만 필터링
    df = df.loc[df['상권업종대분류명'] == '음식']

    # 사용하려는 컬럼만 필터링
    df = df[['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도']]

    # 칼럼명 단순화
    df.columns = ['name',  # 상호명
                  'cate_1',  # 중분류명
                  'cate_2',  # 소분류명
                  'cate_3',  # 표준산업분류명
                  'dong',  # 행정동명
                  'lon',  # 위도
                  'lat'  # 경도
                  ]

    # 카테고리 데이터들을 하나로 묶는 전처리
    df['cate_mix'] = df['cate_1'] + df['cate_2'] + df['cate_3']

    # 텍스트 데이터 피쳐 벡터화를 위해 필요없는 텍스트 '/' 제거
    df['cate_mix'] = df['cate_mix'].str.replace("/", " ")

    # 피쳐 벡터화
    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1, 2))
    place_category = count_vect_category.fit_transform(df['cate_mix'])

    # 코사인 유사도 계산
    place_simi_cate = cosine_similarity(place_category, place_category)

    df['kakao_keyword'] = df['dong'] + "%20" + df['name']
    df['kakao_map_url'] = ''

    # 각 데이터들을 미리 리스트에 담은 다음, 마지막에 데이터 프레임에 합칠 것입니다.

    kakao_map_name_list = []
    blog_review_list = []
    blog_review_qty_list = []
    kakao_map_star_review_stars_list = []
    kakao_map_star_review_qty_list = []

    # 가게별 상세 페이지 url 찾기
    for i, keyword in enumerate(df['kakao_keyword'].tolist()):
        print("이번에 찾을 키워드 :", i, f"/ {df.shape[0]} 행", keyword)
        df.iloc[i, -1] = webCrawler.findUrlinKakaoMap(keyword)

    # 상세 페이지 url에서 원하는 데이터를 추출
    for i, url in enumerate(tqdm_notebook(df['kakao_map_url'])):
        print(f"{i}행 데이터 : {url}")
        reviewData = webCrawler.findReviewInKakaoMapUrl(url)

        blog_review_list.append(reviewData.review_text)
        kakao_map_name_list.append(reviewData.kakao_map_name)
        blog_review_qty_list.append(reviewData.blog_review_qty)
        kakao_map_star_review_stars_list.append(reviewData.star_review_stars)
        kakao_map_star_review_qty_list.append(reviewData.star_review_qty)

    df['kakao_store_name'] = kakao_map_name_list  # 카카오 상세페이지에서 크롤링한 상호명
    df['kakao_star_point'] = kakao_map_star_review_stars_list  # 카카오 상세페이지에서 평가한 별점 평점
    df['kakao_star_point_qty'] = kakao_map_star_review_qty_list  # 카카오 상세페이지에서 별점 평가를 한 횟수
    df['kakao_blog_review_txt'] = blog_review_list  # 카카오 상세페이지에 나온 블로그 리뷰 텍스트들
    df['kakao_blog_review_qty'] = blog_review_qty_list  # 카카오 상세페이지에 나온 블로그 리뷰의 총 개수

    # 리뷰 텍스트 데이터 간의 텍스트 피쳐 벡터라이징
    count_vect_review = CountVectorizer(min_df=2, ngram_range=(1, 2))
    place_review = count_vect_review.fit_transform(df['kakao_blog_review_txt'])

    # 리뷰 텍스트 간의 코사인 유사도 따지기
    place_simi_review = cosine_similarity(place_review, place_review)

    # 공식 1~5의 중요성을 짬뽕시키는 공식
    # * 0.003 등의 가중치를 줘서 조절합니다.

    place_simi_co = (
            + place_simi_cate * 0.3  # 공식 1. 카테고리 유사도
            + place_simi_review * 1  # 공식 2. 리뷰 텍스트 유사도
            + np.repeat([df['kakao_blog_review_qty'].values], len(df['kakao_blog_review_qty']),
                        axis=0) * 0.001  # 공식 3. 블로그 리뷰가 얼마나 많이 올라왔는지
            + np.repeat([df['kakao_star_point'].values], len(df['kakao_star_point']),
                        axis=0) * 0.005  # 공식 4. 블로그 별점이 얼마나 높은지
            + np.repeat([df['kakao_star_point_qty'].values], len(df['kakao_star_point_qty']), axis=0) * 0.001
                                        # 공식 5. 블로그 별점 평가가 얼마나 많이 됐는지
    )

    ## 공공데이터를 활용한 유사도 평가 순위 리스트
    # place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]
    ## 리뷰데이터를 활용한 유사도 평가 순위 리스트
    # place_simi_review_sorted_ind = place_simi_review.argsort()[:, ::-1]
    ## 종합 유사도 평가 순위 리스트
    place_simi_co_sorted_ind = place_simi_co.argsort()[:, ::-1]

    ## 종합 유사도 평사 순위 리스트에서 검색한 상가와 유사도가 높은 상가를 찾는다
    place_index = df[df['name'] == name].index.values
    similar_indexes = place_simi_co_sorted_ind[place_index, :resCount]
    similar_indexes = similar_indexes.reshape(-1)
    return df.iloc[similar_indexes]
