from django.contrib import admin
from .models import *


class UrlModelAdmin(admin.ModelAdmin):
    list_display = ("longurl", "short_url", "hits_counter")


admin.site.register(UrlModel, UrlModelAdmin)


class HitsMetaDataModelAdmin(admin.ModelAdmin):
    list_display = ("short_url", "timestamp")

    def short_url(self, obj):
        return obj.url_model.short_url


admin.site.register(HitsMetaDataModel, HitsMetaDataModelAdmin)
