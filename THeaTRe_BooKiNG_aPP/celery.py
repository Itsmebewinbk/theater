from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE","THeaTRe_BooKiNG_aPP.settings")
app=Celery("THeaTRe_BooKiNG_aPP")

app.conf.enable_utc=False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings,namespace="CELERY")
# app.config_from_object("django.conf:settings",namespace="CELERY")
app.conf.beat_schedule = {
    'add-every-monday-morning':{
        'task': 'Customer.tasks.task.delete_shows',
        'schedule':crontab(minute=00, hour=6),
    }
}
app.autodiscover_tasks()