from django.http import HttpResponse, JsonResponse

def index(request):
    return JsonResponse({
        'data' : "this is main"
    }, json_dumps_params = {'ensure_ascii' : True})