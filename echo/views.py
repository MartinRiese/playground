from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'POST':
        data = request.body
        return HttpResponse(data)
    else:
        return HttpResponse('This view only accepts POST requests.')


@csrf_exempt
def echo_url(request: HttpRequest):
    url = request.build_absolute_uri()
    return JsonResponse({"url": url})
