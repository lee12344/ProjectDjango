from datetime import datetime
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from .models import ChargingStation, Charger

# 충전소 데이터를 가져와 저장하는 함수
def fetch_and_save_charging_stations(api_key):
    # API 엔드포인트 URL
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"

    # API 키 디코딩
    api_key_decode = unquote(api_key)

    # API 요청을 위한 매개변수
    params = {
        "ServiceKey": api_key_decode,
        "pageNo": 1,
        "numOfRows": 2000
    }

    # API에 GET 요청 보내기
    response = requests.get(url, params=params)
    xml = BeautifulSoup(response.text, "xml") #xml 파싱
    items = xml.find_all("item")

    # 주소를 기준으로 충전소를 저장할 딕셔너리
    charging_stations = {}

    # 가져온 아이템들을 순회
    for item in items:
        # XML 응답에서 데이터 추출
        address = item.find("addr").text.strip()
        stat_id = item.find("statId").text.strip()

        # 동일한 주소를 가진 충전소가 이미 존재하는지 확인
        if address not in charging_stations:
            # 새로운 ChargingStation 인스턴스 생성
            station = ChargingStation.objects.create(
                addr=address,
                statNm=item.find("statNm").text.strip(),
                statId=stat_id,
                lat=float(item.find("lat").text.strip()),
                lng=float(item.find("lng").text.strip()),
                useTime=item.find("useTime").text.strip(),
                parkingFree=item.find("parkingFree").text.strip(),
                statUpdDt=datetime.strptime(item.find("statUpdDt").text.strip(), '%Y%m%d%H%M%S')
            )
            # 충전소를 딕셔너리에 추가
            charging_stations[address] = station
        else:
            # 이미 존재하는 충전소인 경우 딕셔너리에서 가져옴
            station = charging_stations[address]

        # charger 데이터
        charger_data = {
            "chgerId": item.find("chgerId").text.strip(),
            "chgerType": item.find("chgerType").text.strip(),
            "stat": item.find("stat").text.strip()
        }

        # 새로운 Charger 인스턴스를 생성하고 충전소와 연결
        charger = Charger.objects.create(
            chgerId=charger_data["chgerId"],
            chgerType=charger_data["chgerType"],
            stat=charger_data["stat"]
        )
        station.charger.add(charger)


