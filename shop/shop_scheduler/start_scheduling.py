from apscheduler.schedulers.background import BackgroundScheduler
from django.db import migrations

from shop.shop_scheduler.get_products_from_zakaz import main_parse
from tzlocal import get_localzone


def start():
    scheduler = BackgroundScheduler(timezone='Europe/Kiev')
    scheduler.add_job(main_parse, 'cron', hour='20', minute='32')
    scheduler.start()
