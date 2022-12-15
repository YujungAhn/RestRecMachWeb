from django.urls import path, include

urlpatterns = [
    path('webCrawler/', include('webCrawler.urls')),
    path('publicData/', include('publicData.urls')),
]
