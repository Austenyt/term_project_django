import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('app.log', encoding='utf-8')  # Указываем кодировку utf-8
handler.setFormatter(formatter)
logger.addHandler(handler)


@util.close_old_connections
def send_mailing(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    message = mailing.message
    clients = mailing.clients.all()

    for client in clients:
        subject = message.subject.encode('utf-8')  # Кодируем строку в байты с использованием utf-8
        send_mail(
            subject=subject,
            message=message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email],
            fail_silently=False,
        )

        # Отправка ответа на сервер после успешной отправки сообщения
        response = f"Рассылка успешно отправлена клиенту {client.email}"
        logger.info(response)

    return HttpResponse("Рассылка завершена успешно")


class Command(BaseCommand):
    help = "Runs APScheduler for sending mailings."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        for mailing in Mailing.objects.filter(status='ready', is_active=True):
            scheduler.add_job(
                send_mailing,
                trigger=CronTrigger(day_of_week=mailing.date.weekday(), hour=mailing.time.hour,
                                    minute=mailing.time.minute),
                id=f"mailing_{mailing.id}",
                args=[mailing.id],
                replace_existing=True,
            )
            logger.info(f"Added job for mailing '{mailing}'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
