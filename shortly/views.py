from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator, ValidationError
from django.views import View
from django.template import loader

from shortly import service
from shortly.models import ShortUrl


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

        short_hash = service.shorten_url(forward_url)

        body = {
            "hash": short_hash
        }
        return JsonResponse(body)



@csrf_exempt
def resolve(request: HttpRequest, slug: str):
    forward_url = service.resolve_hash(slug)
    if forward_url is not None:
        response = HttpResponse(content="", status=303)
        response["Location"] = forward_url
        return response
    else:
        raise ShortUrl.DoesNotExist
