import logging
import typing

from tqdm import tqdm_notebook

import publicData.publicData as publicData
from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도
import webCrawler.webCrawler as webCrawler
import numpy as np
import pandas as pd


def recommandRes(name, areaCd, resCount):
    """
    상권 데이터, 리뷰데이터를 활용해 유사도가 높은 식당을 추천
    name : 식당 이름
    areaCd : 식당의 지역 코드
    resCount :
    """
    # 동별 상권정보 정보 조회
    df = pd.DataFrame(publicData.getAllStoreListInDong(areaCd)) # 메소드 리스트를 가지고 오지 못하는 에러로 dataframe으로 타입 초기화

    rstRow = df[df['상호명'] == name]

    # 음식점 데이터만 필터링 & 조회 속도를 높이기 위해 표준산업 분류명으로 추가 필터링
    df = df[(df['상권업종대분류명'] == '음식') & (df['표준산업분류명'] == rstRow['표준산업분류명'].values[0])]

    # 인덱스 재정렬
    df = df.reset_index(drop=True)

    #######  test   #####################################################
    # # n개 행 만 두고 지우기
    # df = df.truncate(after=20, axis=0)
    # df = df.reset_index(drop=True)
    ###########################################################

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

    df['kakao_keyword'] = df['dong'] + "%20" + df['name']
    df['kakao_map_url'] = ''

    # 가게별 상세 페이지 url 찾기
    webCrawler.initDriver()

    for row in df.itertuples():
        index = row.Index
        keyword = row.name
        print("이번에 찾을 키워드 :", keyword, f"/ {index} 행",)
        print("Row 정보 :", row)
        result = webCrawler.findUrlinKakaoMap(keyword)

        try:
            if pd.isna(result): # string null 체크
                print("Nan Row 정보 :", row)
                df.drop([index], axis=0, inplace=True)
                print("FAil After")
            else:
                df.loc[index, 'kakao_map_url'] = result
                print("Success After :", df.loc[index])
        except Exception as e1:
            print(e1)
            df.drop([index], axis=0, inplace=True)
            print("FAil Before :", )

    # row 드롭 후 인덱스 재정렬
    df = df.reset_index(drop=True)

    # 상세 페이지 url에서 원하는 데이터를 추출
    for i, url in enumerate(tqdm_notebook(df['kakao_map_url'])):
        try:
            print(f"{i}행 데이터 : {url}")
            reviewData = webCrawler.findReviewInKakaoMapUrl(url)

            if pd.isna(reviewData.star_review_qty) or reviewData.star_review_qty == "":  # 별점 평가가 안되는 잘못 조회된 데이터에 대한 처리
                df.drop([i], axis=0, inplace=True)
                continue

            df.loc[i, 'kakao_store_name'] = reviewData.kakao_map_name  # 카카오 상세페이지에서 크롤링한 상호명
            df.loc[i, 'kakao_star_point'] = reviewData.star_review_stars  # 카카오 상세페이지에서 평가한 별점 평점
            df.loc[i, 'kakao_star_point_qty'] = reviewData.star_review_qty  # 카카오 상세페이지에서 별점 평가를 한 횟수
            df.loc[i, 'kakao_blog_review_txt'] = reviewData.review_text  # 카카오 상세페이지에 나온 블로그 리뷰 텍스트들
            df.loc[i, 'kakao_blog_review_qty'] = reviewData.blog_review_qty  # 카카오 상세페이지에 나온 블로그 리뷰의 총 개수

        except Exception as e1:
            print(e1)

    webCrawler.quitDriver()

    # row 드롭 후 인덱스 재정렬
    df = df.reset_index(drop=True)

    # 공백 NaN 데이터 전처리
    mean_value = df['kakao_star_point'].mean()
    df['kakao_star_point'].fillna(mean_value, inplace=True)
    df['kakao_star_point_qty'].fillna(0, inplace=True)
    df['kakao_blog_review_qty'].fillna(0, inplace=True)

    # 카테고리 데이터들을 하나로 묶는 전처리
    df['cate_mix'] = df['cate_1'] + df['cate_2'] + df['cate_3']

    # 텍스트 데이터 피쳐 벡터화를 위해 필요없는 텍스트 '/' 제거
    df['cate_mix'] = df['cate_mix'].str.replace("/", " ")

    # 피쳐 벡터화
    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1, 2))
    place_category = count_vect_category.fit_transform(df['cate_mix'])

    # 코사인 유사도 계산
    place_simi_cate = cosine_similarity(place_category, place_category)

    # 리뷰 텍스트 데이터 간의 텍스트 피쳐 벡터라이징
    count_vect_review = CountVectorizer(min_df=2, ngram_range=(1, 2))
    place_review = count_vect_review.fit_transform(df['kakao_blog_review_txt'].astype(str))

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
    similar_indexes = place_simi_co_sorted_ind[place_index, :resCount+1] # 출력을 원하는 유사한 음식점의 개수
    similar_indexes = similar_indexes.reshape(-1)
    return df.iloc[similar_indexes]
