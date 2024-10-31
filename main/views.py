from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from ..publicData import publicData


# def index(request):
#     return JsonResponse({
#         'data' : "this is main"
#     }, json_dumps_params = {'ensure_ascii' : True})


# def home(request):
#     sido_data = publicData.getCtprvnCds()
#     return render(request, 'home.html', {'sido_data': sido_data})
#
# def public_data(request, user_id):
#     # user_id 등을 사용해서 데이터 조회 수행
#     context = {
#         'user_id': user_id,
#     }
#
#     return render(request, 'user_detail.html', context)
# def prediction(request):
#     return JsonResponse({
#         'data' : "precision"
#     }, json_dumps_params = {'ensure_ascii' : True})



