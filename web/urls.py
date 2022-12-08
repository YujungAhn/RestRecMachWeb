from .webCrawler import webCrawlerViews
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webCrawler/', webCrawlerViews.index),
    path('test/', webCrawlerViews.test),
]
