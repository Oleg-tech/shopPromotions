from apscheduler.schedulers.background import BackgroundScheduler

from shop.shop_scheduler.get_products import parse_manager


def start():
    scheduler = BackgroundScheduler(timezone='Europe/Kiev')
    scheduler.add_job(parse_manager, 'cron', hour='12', minute='42')
    scheduler.start()
