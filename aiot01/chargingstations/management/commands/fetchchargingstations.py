from ...utils import fetch_and_save_charging_stations
from django.core.management.base import BaseCommand

# 관리 명령에 대한 도움말 텍스트
class Command(BaseCommand):
    help = 'Fetch charging stations data and save to database'

#API 키를 사용하여 함수를 호출
    def handle(self, *args, **kwargs):
        api_key = "EpUhD8WnDkKZKfH5rj1U7C9Y5hCObQbwGjbEU00ZYw0lWevnETv7%2BlHjECr%2F0%2BJaWN9K1SW10Fzj8IsBkaGOWQ%3D%3D"
        fetch_and_save_charging_stations(api_key)
