from django.urls import path
from . import views

urlpatterns = [
    path('getCtprvnCds/', views.getCtprvnCds, name='getCtprvnCds'),
    # # 패스 파라미터 방식과/ 쿼리 파라미터 방식중에 뭐가 더 좋은지 혜원이랑 이야기하고 검토
    # # 패스 파라미터
    # path('getSignguCds/<int:user_id>', views.getCtprvnCds, name='getSignguCds'),
    # 쿼리 파라미터
    path('getSignguCds', views.getSignguCds, name='getSignguCds'),
    path('getAdongCds', views.getAdongCds, name='getAdongCds'),
    path('main/', views.main_view, name='main'),  # 새로운 URL 추가
]