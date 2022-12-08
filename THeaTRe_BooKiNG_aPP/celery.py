from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE","theatre_booking_app.settings")
app=Celery("theatre_booking_app")
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.enable_utc=False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings,namespace="CELERY")
# app.config_from_object("django.conf:settings",namespace="CELERY")

#CELERY BEAT SETTING

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.on_after_configure.connect()
def trigger_autodiscovery(sender, **kwargs):
    app.loader.import_default_modules()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

