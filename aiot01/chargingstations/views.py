# views.py
from rest_framework import generics
from .models import ChargingStation
from .serializers import ChargingStationSerializer

# ChargingStation 모델의 목록 조회 및 생성을 다루는 뷰
class ChargingStationListCreateView(generics.ListCreateAPIView):
    # 모든 ChargingStation 인스턴스를 대상으로 하는 쿼리셋
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer

