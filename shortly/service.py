import secrets
from shortly.models import ShortUrl


def shorten_url(forward_url):
    short_hash = secrets.token_urlsafe(8)
    short_url = ShortUrl(hash=short_hash, forward_url=forward_url)
    short_url.save()
    return short_hash


def resolve_hash(url_hash):
    short_urls = ShortUrl.objects.filter(hash=url_hash)
    if len(short_urls) > 0:
        return short_urls[0].forward_url
    else:
        return None
