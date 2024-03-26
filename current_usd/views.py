from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from .models import CurrentUsd
from .serializers import CurrentUsdSerializer


class CurrentUsdAPIView(APIView):
    def get(self, request):
        out_request = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()#запрос к сайту цб
        price = float(out_request["Valute"]["USD"]["Value"]) #получаем последнюю цену доллара из словаря цб
        data = {"price": price} #данные для создания новой записи

        serializer = CurrentUsdSerializer(data=data)
        serializer.is_valid()
        if serializer.validate_date_request(value=data): #проверка на время записи (>10сек)
            #если прошло более 10сек с момента посленей записи, сохраняем данные в бд
            serializer.save()

        try:
            '''Получем послежние 10 записей в бд и возвражаем их в качестве ответа на запрос'''
            last_ten_requests = CurrentUsd.objects.all().order_by('-id')[:10]
            return Response(CurrentUsdSerializer(last_ten_requests, many=True).data)
        except:
            #Исключение ошибки list out of range (если в бд менее 10 записей, возвращаем все записи)
            last_requests = CurrentUsd.objects.all().order_by('-id')
            return Response(CurrentUsdSerializer(last_requests, many=True).data)