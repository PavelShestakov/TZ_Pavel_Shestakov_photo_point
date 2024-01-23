from rest_framework import serializers
from .models import CurrentUsd
import datetime

class CurrentUsdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentUsd
        fields = ['price', 'date_request']

    def validate_date_request(self, value):
        """Проверка записей на время записи, пауза между запросами курсов должна быть не менее 10 секунд"""
        datetime_of_last_entry = CurrentUsd.objects.all().order_by('-id').values('date_request')
        if datetime_of_last_entry:
            """Если какая-либо запись присутствует, проверяем чтобы она была старше минимум на 10 сек чем текущее время"""
            datetime_of_last_entry = datetime_of_last_entry[0]['date_request'] #время последней записи в бд (utc)
            now_time = datetime.datetime.now(datetime.timezone.utc) # текущее время utc
            time_difference = now_time - datetime_of_last_entry # разница времени
            if time_difference.seconds<=10:
                #С момента последней записи прошло менее 10 секунд
                return False
        return value

    def create(self, validated_data):
        return CurrentUsd.objects.create(**validated_data)
