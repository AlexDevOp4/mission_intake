import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mission_intake.settings.local")

app = Celery("mission_intake")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
