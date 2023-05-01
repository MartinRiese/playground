from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import secrets
from shortly.models import ShortUrl
from django.core.validators import URLValidator, ValidationError

@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'POST':
        forward_url = request.body.decode()
        try:
            URLValidator()(forward_url)
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

        short_hash = secrets.token_urlsafe(8)
        short_url = ShortUrl(hash=short_hash, forward_url=forward_url)
        short_url.save()

        body = {
            "hash": short_hash
        }
        return JsonResponse(body)
    else:
        return HttpResponseBadRequest('This view only accepts POST requests.')

@csrf_exempt
def resolve(request: HttpRequest, slug: str):
    try:
        short_urls = ShortUrl.objects.filter(hash=slug)
        if len(short_urls) < 1:
            raise ShortUrl.DoesNotExist
        response = HttpResponse(content="", status=303)
        response["Location"] = short_urls[0].forward_url
        return response
    except ShortUrl.DoesNotExist:
        return HttpResponseNotFound(f"Could not find slug : {slug}")
