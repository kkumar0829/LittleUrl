from itertools import count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from littleurl import constants
from myurl.serializers import UrlSerializer
from myurl.utils import get_shortend_url
from .models import *
from datetime import datetime, timedelta


class UrlShortnerCreateView(APIView):
    def post(self, request):
        # Serialize the user input data
        serializer = UrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save long url with serializer validated data
        instance = serializer.save()
        hash_id = constants.LONG_NUMBER_ID + serializer.data.get('id')
        short_url = get_shortend_url(hash_id)
        short_url = constants.BASE_SHORTNER_URL + short_url
        # Update instance with short url, to be used at later point of time
        instance.short_url = short_url
        instance.save()
        # Return short url to client
        return Response({
            "short_url": short_url
        }, status=status.HTTP_200_OK)


class GetLongUrl(APIView):
    def get(self, request, short_url):
        short_url = "http://localhost:8000/" + str(short_url)
        longurl = UrlModel.objects.get(short_url=short_url).longurl
        url_model = UrlModel.objects.get(short_url=short_url)
        hits = UrlModel.objects.get(short_url=short_url).hits_counter
        hits = hits + 1
        UrlModel.objects.filter(short_url=short_url).update(hits_counter=hits)
        HitsMetaDataModel.objects.create(timestamp=datetime.now(), url_model=url_model)

        return Response("Your Url : " + longurl)


class GetUrlMetaData(APIView):
    def get(self, request, short_url):
        short_url = "http://localhost:8000/" + str(short_url)
        hits = UrlModel.objects.get(short_url=short_url).hits_counter
        current_time = datetime.now()
        hour_back_time = datetime.now() - timedelta(hours=1)
        hit_list = HitsMetaDataModel.objects.filter(url_model__short_url=short_url, timestamp__gte=hour_back_time,
                                                    timestamp__lte=current_time)
        return Response({
            "total_hit": f"Total Hits of Your Url : {hits}",
            "last_hour_hit": "Total Hits of Your Url in last 1 hour : " + str(len(hit_list))
        })


class SearchUrl(APIView):
    def get(self, request, search_string):
        res = UrlModel.objects.raw(f"select id, longurl from myurl_urlmodel where longurl like '%{search_string}%'")
        response_json = []
        for url_model in res:
            response_json.append({
                "long_url": url_model.longurl,
                "total_hit": url_model.hits_counter
            })
        return Response(response_json)
