# Standard Library
import os

# Third Party Stuff
import environ
from celery import Celery
 

env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')
app = Celery("chat_app")

if "CELERY_RESULT_BACKEND" in env:
    app.conf.result_backend = env("CELERY_RESULT_BACKEND")
    app.conf.result_expires = env("CELERY_RESULT_BACKEND_EXPIRY", default=1200)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

