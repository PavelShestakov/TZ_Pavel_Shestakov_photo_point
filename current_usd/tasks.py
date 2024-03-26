# Create your tasks here
#from celery.schedules import crontab
from celery import shared_task

import requests
#from time import sleep
#from celery import shared_task
#from current_usd.tasks import test
@shared_task
def test():
    print("Kellp")
    return "Hello"

@shared_task
def conductor():
    requests.get('http://127.0.0.1:8000/get-current-usd/')
    return "Hello"
