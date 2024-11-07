from django.urls import path
from . import views

urlpatterns = [
    path('getCtprvnCds/', views.getCtprvnCds, name='getCtprvnCds'),
    path('main/', views.main_view, name='main'),  # 새로운 URL 추가
]