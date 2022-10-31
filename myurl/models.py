from datetime import datetime
from django.utils.timezone import now
from django.db import models


class UrlModel(models.Model):
    longurl = models.URLField()
    short_url = models.URLField(default="")
    hits_counter = models.IntegerField(default=0)


class HitsMetaDataModel(models.Model):
    url_model = models.ForeignKey(UrlModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


