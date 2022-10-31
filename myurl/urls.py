from django.urls import path

from .views import *


urlpatterns = [
    path('url-shortner/', UrlShortnerCreateView.as_view()),
    path('<str:short_url>', GetLongUrl.as_view()),
    path('<str:short_url>/info/', GetUrlMetaData.as_view()),
    path('search/<str:search_string>', SearchUrl.as_view()),

]
