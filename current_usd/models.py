from django.db import models

class CurrentUsd(models.Model):
    price = models.FloatField() #цена доллара
    date_request = models.DateTimeField(auto_now_add=True) #время создания записи

    def __str__(self):
        return f"USD/RUB {self.date_request}: {self.price}"
