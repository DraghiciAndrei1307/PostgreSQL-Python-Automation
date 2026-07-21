import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings')

app = Celery('django_api', broker='redis://localhost:6379/0')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()