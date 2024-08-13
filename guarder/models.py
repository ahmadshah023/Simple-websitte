from django.db import models


class ShortenedURL(models.Model):
    original_url = models.URLField()
    shortened_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shortened_url


# Create your models here.
class Guarder(models.Model):
    name = models.CharField(max_length=100)
