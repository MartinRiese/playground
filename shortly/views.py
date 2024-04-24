from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import secrets
from shortly.models import ShortUrl
from django.core.validators import URLValidator, ValidationError
from django.views import View
from django.template import loader


@method_decorator(csrf_exempt, name='dispatch')
class ShortlyView(View):

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseBadRequest('This view only accepts POST requests.')

    def get(self, request):
        template = loader.get_template('shortly/index.html')
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
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
