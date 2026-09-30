from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_sale_time_every_2_minutes": {
        "task": "flash_sales.tasks.sale_pre_warming",
        "schedule": 120.0,
    },
    "check_sale_end_time_every_minute": {
        "task": "flash_sales.tasks.item_sale_ender",
        "schedule": 60.0,
    },
    "sync_redis_to_postgres_every_10_secs": {
        "task": "flash_sales.tasks.sync_redis_to_postgres",
        "schedule": 10.0,
    },
    "change_expire_orders_status_every_1_minutes": {
        "task": "orders.tasks.check_and_change_order_status",
        "schedule":120.0,
    },
}
