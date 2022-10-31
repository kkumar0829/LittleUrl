from rest_framework import serializers
from .models import UrlModel


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlModel
        fields = '__all__'
