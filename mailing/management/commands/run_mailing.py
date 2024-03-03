import logging
from datetime import timedelta
from smtplib import SMTPException

from django.utils import timezone

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util

from mailing.models import Mailing

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('app.log')
handler.setFormatter(formatter)
logger.addHandler(handler)


@util.close_old_connections
def send_mailing(mailing_id):
    """
        Отправляет рассылку по указанному идентификатору.

    """
    mailing = Mailing.objects.get(pk=mailing_id)
    message = mailing.message
    clients = mailing.clients.all()

    for client in clients:
        subject = message.subject
        send_mail(
            subject=subject,
            message=message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email],
            fail_silently=False,
        )

        # Отправка ответа на сервер после успешной отправки сообщения
        response = f"Рассылка успешно отправлена клиенту {client.email}"
        print(response)
        logger.info(response)

    return HttpResponse("Рассылка завершена успешно")


class Command(BaseCommand):
    """
        Команда для запуска планировщика задач APScheduler для отправки рассылок.

    """
    help = "Runs APScheduler for sending mailings."

    def handle(self, *args, **options):
        """
                Обработка команды.

        """
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        now = timezone.now()
        start = now.replace(second=0, microsecond=0)
        end = start + timedelta(minutes=1)

        mailings = Mailing.objects.filter(time__gte=start, time__lt=end).exclude(status='pending')

        for mailing in mailings:
            subject = mailing.message.subject
            body = mailing.message.body
            recipients = list(mailing.clients.values_list('email', flat=True))

            mailing.status = 'pending'
            mailing.save()

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=False
                )
            except SMTPException as e:
                # Обработка исключения
                logger.error(f"Failed to send mailing '{mailing}': {e}")
            else:
                # Отправка прошла успешно
                logger.info(f"Mailing '{mailing}' sent successfully.")
                mailing.time = mailing.time + timedelta(days=1)
                mailing.status = 'ready'
                mailing.save()
            print(f"Mailing processed for '{mailing}'.")

        print(f"Mailings processed for {start}-{end}")

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
            print(f"Added job for mailing '{mailing}'.")

        try:
            logger.info("Starting scheduler...")
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
