from django.db import models

class Charger(models.Model):
    chgerId = models.CharField(max_length=50)
    chgerType = models.CharField(max_length=50)
    stat = models.CharField(max_length=50)

    class Meta:
        db_table = "Charger"

class ChargingStation(models.Model):
    addr = models.CharField(max_length=255, null=True)
    statNm = models.CharField(max_length=100, null=True)
    statId = models.CharField(max_length=50, null=True)
    charger = models.ManyToManyField(Charger)  # Charger 모델과의 ManyToMany 관계 설정, 다대다 관계 설정
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    useTime = models.CharField(max_length=50, null=True)
    parkingFree = models.CharField(max_length=50, null=True)
    statUpdDt = models.DateTimeField(auto_now=True, null=True)  # 변경 시간대 정보 자동 갱신

    class Meta:
        db_table = "Station"
