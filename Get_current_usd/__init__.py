# django_celery/__init__.py
from Get_current_usd.celery import app as celery_app

__all__ = ("celery_app",)