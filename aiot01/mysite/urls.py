from django.urls import path, include
from django.contrib import admin
# url 패턴 정의
urlpatterns = [
    # ...
    path('api/', include('chargingstations.urls')),

    # ...
]