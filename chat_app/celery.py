# Standard Library
import os

# Third Party Stuff
import environ
from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings.base')
app = Celery("vibe_core")

if "CELERY_RESULT_BACKEND" in env:
    app.conf.result_backend = env("CELERY_RESULT_BACKEND")
    app.conf.result_expires = env("CELERY_RESULT_BACKEND_EXPIRY", default=1200)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

