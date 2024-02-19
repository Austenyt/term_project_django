import os
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from service.models import Mailing


class Command(BaseCommand):
    help = 'Send mailings'

    def handle(self, *args, **options):
        mailings = Mailing.objects.all()

        for mailing in mailings:
            subject = mailing.message.subject
            message = mailing.message.body
            recipients = [client.email for client in mailing.recipients.all()]

            send_mail(subject, message, 'your_email@example.com', recipients)

            self.stdout.write(self.style.SUCCESS(f'Successfully sent mailing "{subject}" to {", ".join(recipients)}'))
