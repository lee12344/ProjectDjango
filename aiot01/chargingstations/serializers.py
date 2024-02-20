# chargingstations/api/serializers.py
from rest_framework import serializers
from .models import ChargingStation, Charger

# Charger 모델을 위한 Serializer
class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        # Serializer에 포함할 필드들을 명시 ('chgerId', 'stat', 'chgerType')
        fields = ['chgerId','stat','chgerType']

# ChargingStation 모델을 위한 Serializer
class ChargingStationSerializer(serializers.ModelSerializer):
    # 연관된 Charger 인스턴스들을 다루기 위해 ChargerSerializer 사용 (다수 여부 명시)
    charger = ChargerSerializer(many=True)
    class Meta:
        model = ChargingStation
        # ChargingStation 모델의 모든 필드를 직렬화 대상에 포함 ('__all__')
        fields = '__all__'
