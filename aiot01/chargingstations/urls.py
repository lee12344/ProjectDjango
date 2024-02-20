# chargingstations/urls.py
from django.urls import path
from .views import ChargingStationListCreateView

# url 패턴 정의
urlpatterns = [
# 'charging-stations/' 경로에 ChargingStationListCreateView를 사용하여 뷰 호출
    path('charging-stations/', ChargingStationListCreateView.as_view(), name='charging-stations'),
]