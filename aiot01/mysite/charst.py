import pandas as pd
import requests
from urllib import parse
from bs4 import BeautifulSoup


url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
api_key_utf8 = "EpUhD8WnDkKZKfH5rj1U7C9Y5hCObQbwGjbEU00ZYw0lWevnETv7%2BlHjECr%2F0%2BJaWN9K1SW10Fzj8IsBkaGOWQ%3D%3D"
api_key_decode = parse.unquote(api_key_utf8)

parms = {
    "ServiceKey": api_key_decode,
    "pageNo":1,
    "numOfRows":5
}

response = requests.get(url,params=parms)
xml = BeautifulSoup(response.text,"xml")
items = xml.find("items")
item_list = []
for item in items:
    item_dict = {
        '주소':item.find("addr").text.strip(),
        '충전소명':item.find("statNm").text.strip(),
        '충전소ID':item.find("statId").text.strip(),
        '충전기ID':item.find("chgerId").text.strip(),
        '충전기타입':item.find("chgerType").text.strip(),
        '위도':item.find("lat").text.strip(),
        '경도':item.find("lng").text.strip(),
        '이용가능시간':item.find("useTime").text.strip(),
        '주차료': item.find("parkingFree").text.strip(),
    }
    item_list.append(item_dict)

    df = pd.DataFrame(item_list)
    print(df.iloc[-1])