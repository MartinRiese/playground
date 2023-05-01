from django.db import models

class ShortUrl(models.Model):
    hash = models.SlugField(max_length=10)
    forward_url = models.CharField(max_length=500)