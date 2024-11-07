from django.shortcuts import render
from django.http import JsonResponse
from publicData import publicData

# Create your views here.


def getCtprvnCds(request):
    data = publicData.getCtprvnCds()

    # 필요한 데이터만 추출
    filtered_data = [{"code": item["ctprvnCd"], "name": item["ctprvnNm"]} for item in data['body']['items']]
    response_data = {"items": filtered_data}

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}) # ensure_ascii 한글 처리


def main_view(request):
    return render(request, 'rec_res/main.html')