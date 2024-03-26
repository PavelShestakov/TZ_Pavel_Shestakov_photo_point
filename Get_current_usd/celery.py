import os
from celery import Celery
# https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Get_current_usd.settings")
app = Celery("Get_current_usd") #"Get_current_usd"
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')