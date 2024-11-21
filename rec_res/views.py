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


def getSignguCds(request):
    ctprvnCd = request.GET.get('ctprvnCd')  # 쿼리 파라미터에서 user_id 가져오기
    if ctprvnCd:
        try:
            data = publicData.getSignguCds(ctprvnCd)

            # 필요한 데이터만 추출
            filtered_data = [{"code": item["signguCd"], "name": item["signguNm"]} for item in data['body']['items']]
            response_data = {"items": filtered_data}

            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})  # ensure_ascii 한글 처리
        except:
            return JsonResponse({'error': '데이터를 찾을 수 없습니다.'}, status=404)
    else:
        return JsonResponse({'error': '시도 설정이 필요합니다.'}, status=400)


def getAdongCds(request):
    signguCd = request.GET.get('signguCd')  # 쿼리 파라미터에서 user_id 가져오기
    if signguCd:
        try:
            data = publicData.getAdongCds(signguCd)

            # 필요한 데이터만 추출
            filtered_data = [{"code": item["adongCd"], "name": item["adongNm"]} for item in data['body']['items']]
            response_data = {"items": filtered_data}

            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})  # ensure_ascii 한글 처리
        except:
            return JsonResponse({'error': '데이터를 찾을 수 없습니다.'}, status=404)
    else:
        return JsonResponse({'error': '시도 설정이 필요합니다.'}, status=400)



def main_view(request):
    return render(request, 'rec_res/main.html')