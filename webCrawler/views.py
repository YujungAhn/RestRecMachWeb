from django.http import HttpResponse, JsonResponse

def index(request):
    return JsonResponse({
        'data' : "this is webCrawler"
    }, json_dumps_params = {'ensure_ascii' : True})