from django.urls import include, path
from . import views

# 요청을 알맞은 뷰로 전달
urlpatterns = [
    path('rec_res/', include('rec_res.urls')),  # myapp의 URL 포함
    # path('', views.index),
    # path('', views.home, name='home'),
    # path('api/', include('rest_framework.urls')), # RESTful API를 쉽게 만들도록 돕는  app
    # path('', views.index), # views의 index 함수와 연결
    # path('publicdata/<int:user_id>/', views.public_data, name='public_data'), # 시/군구/동 - 파라미터로 전달받기
    # path('publicdata/<int:user_id>/', views.public_data, name='public_data'), # 시/군구/동 - 파라미터로 전달받기
    # path('', views.prediction), # 동

]
