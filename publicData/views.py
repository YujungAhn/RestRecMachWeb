from django.http import HttpResponse, JsonResponse

def index(request):
    return JsonResponse({
        'data' : "this is publicData"
    }, json_dumps_params = {'ensure_ascii' : True})