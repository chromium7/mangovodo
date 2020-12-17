import os
from celery import Celery

# Set the default django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings.production')

app = Celery('mangovodo')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
