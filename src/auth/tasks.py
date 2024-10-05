import smtplib
from celery import shared_task

from src.config import settings


@shared_task
def send_mail_code(email, code):
    subject = "Confirmation code"
    body = f"Your confirmation code to finish the registration: {code}"
    msg = f'Subject: {subject}\n\n'
    msg += body
    with smtplib.SMTP(settings.smtp.host, settings.smtp.port) as server:
        server.starttls()
        server.login(settings.smtp.host_user, settings.smtp.host_password,)
        server.sendmail(settings.smtp.host_user, email, msg)
