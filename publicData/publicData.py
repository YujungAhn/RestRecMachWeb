import pandas as pd
import requests

from common import rParser
from publicData.ServiceKey import KEY
import json

def getStoreListInDong(pageNo, numOfRows, areaCategory, areaCd)-> json:
    """
    행정동 단위 상가업소 조회
    pageNo        # 페이지 번호
    numOfRows     # 한 페이지 결과 수
    areaCategory  # 구분 ID (시도는 ctprvnCd, 시군구는 signguCd, 행정동은 adongCd를 사용)
    areaCd        # 행정 구역 코드 (시도코드값, 시군구코드값, 행정동코드값)

    ## 응답 메세지 명세
    결과코드	resultCode	2	필수	00	결과코드
    결과메시지	resultMsg	50	필수	OK	결과메시지
    한 페이지 결과 수	numOfRows	4	필수	10	한 페이지 결과 수
    페이지 번호	pageNo	4	필수	1	페이지번호
    전체 결과 수	totalCount	4	필수	3	전체 결과 수
    데이터 설명	description	30	필수	202106	데이터 설명
    컬럼	columns	300	필수	00	컬럼
    기준년월	stdrYm	6	필수	NORMAL SERVICE	기준년월
    상가업소번호	bizesId	20	필수	10142096	해당 상가업소에 부여된 일련번호
    상호명	bizesNm	100	필수	***스타	해당 상가업소의 상호명
    지점명	brchNm	50	옵션	***서울	해당 상가업소가 지점인 경우 지점명
    상권업종대분류코드	indsLclsCd	1	필수	Q	해당 상가업소의 상권업종대분류코드
    상권업종대분류명	indsLclsNm	40	필수	음식	해당 상가업소의 상권업종대분류명
    상권업종중분류코드	indsMclsCd	3	필수	Q12	해당 상가업소의 상권업종중분류코드
    상권업종중분류명	indsMclsNm	40	필수	커피점/카페	해당 상가업소의 상권업종중분류명
    상권업종소분류코드	indsSclsCd	6	필수	Q12A01	해당 상가업소의 상권업종소분류코드
    상권업종소분류명	indsSclsNm	40	필수	커피전문점/카페/다방	해당 상가업소의 상권업종소분류명
    표준산업분류코드	ksicCd	5	옵션	I56220	해당 상가업소의 표준산업분류코드
    표준산업분류명	ksicNm	40	옵션	비알콜 음료점업	해당 상가업소의 표준산업분류코드에 대한 명칭
    시도코드	ctprvnCd	2	옵션	11	해당 상가업소의 시도 코드
    시도명	ctprvnNm	20	옵션	서울특별시	해당 상가업소의 시도 명칭
    시군구코드	signguCd	5	옵션	11680	해당 상가업소의 시군구 코드
    시군구명	signguNm	20	옵션	강남구	해당 상가업소의 시군구 명칭
    행정동코드	adongCd	10	옵션	1168056500	해당 상가업소의 행정동 코드
    행정동명	adongNm	20	옵션	청담동	해당 상가업소의 행정동 명칭
    법정동코드	ldongCd	10	옵션	1168010400	해당 상가업소의 법정동 코드
    법정동명	ldongNm	20	옵션	청담동	해당 상가업소의 법정동 명칭
    PNU코드	lnoCd	19	옵션	1168010400200530007	해당 상가업소 지번주소에 해당하는 PNU코드
    대지구분코드	plotSctCd	1	옵션	1	해당 상가업소 지번주소의 대지구분 코드(1:대지, 2:산)
    대지구분명	plotSctNm	2	옵션	대지	해당 상가업소 지번주소의 대지구분 코드명(대지, 산)
    지번본번지	lnoMnno	4	옵션	53	해당 상가업소 지번주소의 본번지
    지번부번지	lnoSlno	4	옵션	7	해당 상가업소 지번주소의 부번지
    지번주소	lnoAdr	100	옵션	서울특별시 강남구 청담동 53-7	해당 상가업소 지번기준 전체주소
    도로명코드	rdnmCd	12	옵션	116802122002	해당 상가업소 도로명주소 도로명코드
    도로명	rdnm	30	옵션	서울특별시 강남구 영동대로	해당 상가업소 도로명주소 도로명코드에 대한 명칭
    건물본번지	bldMnno	5	옵션	737	해당 상가업소 도로명주소 기준 건물 본번지
    건물부번지	bldSlno	5	옵션		해당 상가업소 도로명주소 기준 건물 부번지
    건물관리번호	bldMngNo	25	옵션	1168010400100530007017901	해당 상가업소 도로명주소 기준 건물관리번호
    건물명	bldNm	40	옵션	*****	해당 상가업소 도로명주소 기준 건물명
    도로명주소	rdnmAdr	100	옵션	서울특별시 강남구 영동대로 737	해당 상가업소 도로명 주소기준 전체주소
    구우편번호	oldZipcd	6	옵션	135952	해당 상가업소 구우편번호(개편전 우편번호)
    신우편번호	newZipcd	5	옵션	06071	해당 상가업소 신우편번호(개편후 우편번호)
    동정보	dongNo	10	옵션		해당 상가업소가 소재한 동정보
    층정보	flrNo	10	옵션	1	해당 상가업소가 소재한 층정보
    호정보	hoNo	10	옵션		해당 상가업소가 소재한 호정보
    경도	lon	22	옵션	127.05416	해당 상가업소의 WGS84기준 위도 좌표값
    위도	lat	22	옵션	37.52375	해당 상가업소의 WGS84기준 위도 좌표값
    """

    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong'
    # 필수 parameter
    params = {'serviceKey': KEY}    # 인증키
    params['pageNo'] = pageNo       # 페이지 번호
    params['numOfRows'] = numOfRows # 한 페이지 결과 수
    params['divId'] = areaCategory  # 구분 ID (시도는 ctprvnCd, 시군구는 signguCd, 행정동은 adongCd를 사용)
    params['key'] = areaCd          # 행정 구역 코드 (시도코드값, 시군구코드값, 행정동코드값)

    # 옵션 parameter
    # params['indsLclsCd'] = 'Q'       # 입력된 대분류 업종에 해당하는 것만 조회
    # params['indsMclsCd'] = 'Q12'     # 입력된 중분류 업종에 해당하는 것만 조회
    # params['indsSclsCd'] = 'Q12A01'  # 입력된 소분류 업종에 해당하는 것만 조회
    params['type'] = 'json'            # xml / json

    result = requests.get(url, params=params).json()

    return result


def getCtprvnCds():
    """
    시도 코드 조회

    ## 응답 메세지 명세
    데이터 설명	description	30	필수	소상공인시장진흥공단 상권정보 시군구 코드	데이터 설명
    컬럼	columns	300	필수	시도코드..	컬럼
    결과코드	resultCode	2	필수	00	결과코드
    결과메세지	resultMsg	50	필수	NORMAL SERVICE	결과메세지
    시도코드	ctprvnCd	2	필수	11	시도코드
    시도명	ctprvnNm	10	필수	서울특별시	시도명
    데이터기준일자	stdrDt	10	필수	2020-12-31	데이터 배포일자
    """

    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi'
    params = {'serviceKey': KEY}  # 인증키
    params['resId'] = 'dong'      # 리소스에 대한 ID. dong은 행정구역 리소스를 나타냄
    params['catId'] = 'mega'      # 리소스에서 카테고리를 구분하는 항목. mega는 시도에 해당
    params['type'] = 'json'       # 데이터 유형 (xml, json)

    result = requests.get(url, params=params).json()

    return result


def getSignguCds(ctprvnCd):
    """
    시군구코드 조회
    ctprvnCd 시도코드

    ## 응답 메세지 명세
    데이터 설명	description	30	필수	소상공인시장진흥공단 상권정보 시군구 코드	데이터 설명
    컬럼	columns	300	필수	시도코드..	컬럼
    결과코드	resultCode	2	필수	00	결과코드
    결과메세지	resultMsg	50	필수	NORMAL SERVICE	결과메세지
    시도코드	ctprvnCd	2	필수	11	시도코드
    시도명	ctprvnNm	10	필수	서울특별시	시도명
    시군구코드	signguCd	5	필수	11740	시군구코드
    시군구명	signguNm	10	필수	강동구	시군구명
    데이터기준일자	stdrDt	10	필수	2020-12-31	데이터 배포일자
    """

    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi'
    params = {'serviceKey': KEY}   # 인증키
    params['resId'] = 'dong'       # 리소스에 대한 ID. dong은 행정구역 리소스를 나타냄
    params['catId'] = 'cty'        # 리소스에서 카테고리를 구분하는 항목. cty는 시군구에 해당
    params['ctprvnCd'] = ctprvnCd  # 시도코드 입력
    params['type'] = 'json'         # 데이터 유형 (xml, json)

    result = requests.get(url, params=params).json()

    return result


def getAdongCds(signguCd):
    """
    행정동코드 조회
    signguCd 시군구코드

    ## 응답 메세지 명세
    데이터 설명	description	30	필수	소상공인시장진흥공단 상권정보 시군구 코드	데이터 설명
    컬럼	columns	300	필수	시도코드..	컬럼
    결과코드	resultCode	2	필수	00	결과코드
    결과메세지	resultMsg	50	필수	NORMAL SERVICE	결과메세지
    시도코드	ctprvnCd	2	필수	11	시도코드
    시도명	ctprvnNm	10	필수	서울특별시	시도명
    시군구코드	signguCd	5	필수	11740	시군구코드
    시군구명	signguNm	10	필수	강동구	시군구명
    행정동코드	adongCd	10	필수	1174051500	행정동코드
    행정동명	adongNm	10	필수	강일동	행정동명
    데이터기준일자	stdrDt	10	필수	2020-12-31	데이터 배포일자
    """

    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi'
    params = {'serviceKey': KEY}   # 인증키
    params['resId'] = 'dong'       # 리소스에 대한 ID. dong은 행정구역 리소스를 나타냄
    params['catId'] = 'admi'       # 리소스에서 카테고리를 구분하는 항목. admi는 행정동에 해당
    params['signguCd'] = signguCd  # 시군구코드 입력
    params['type'] = 'json'         # 데이터 유형 (xml, json)

    result = requests.get(url, params=params).json()

    return result


def getAllStoreListInDong(areaCd):
    """
    행정동 단위 상가업소 전체 조회
    areaCd        # 행정동 코드 값
    """

    endFlag = False
    pageCount = 1
    pageRowSize = 10000
    jsonName = 'items'

    result_data = []

    while endFlag is False:
        pageCount += 1
        storeList = getStoreListInDong(pageCount, pageRowSize, 'adongCd', areaCd)
        jsonData = storeList['body']

        if not jsonData.get(jsonName):
            endFlag = True
        else:
            data = rParser.convertJsonToDataframe(jsonData, jsonName)
            result_data.append(data)

    result_data = pd.concat(result_data)

    return result_data


