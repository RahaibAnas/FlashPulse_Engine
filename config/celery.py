from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_sale_time_every_2_minutes": {
        "task": "flash_sales.tasks.sale_pre_warming",
        "schedule":120.0
    }
}
