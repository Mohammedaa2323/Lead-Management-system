from celery import shared_task
from django.core.management import call_command

@shared_task
def send_daily_summary():
    call_command('send_daily_summary')