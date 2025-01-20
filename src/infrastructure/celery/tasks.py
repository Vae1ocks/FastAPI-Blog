import logging
import smtplib
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_email(
    host: str,
    host_user: str,
    host_password: str,
    port: int,
    emails: list[str],
    subject: str,
    message: str,
):
    msg = f"Subject: {subject}\n\n"
    msg += message

    with smtplib.SMTP(host, port) as server:
        try:
            server.starttls()
            server.login(host_user, host_password)
            server.sendmail(host_user, emails, msg)
            logger.debug("Email sent successfully")
        except smtplib.SMTPRecipientsRefused:
            logger.warning("Exception smtplib.SMTPRecipientsRefused when sending mail")
        except Exception as e:  # noqa
            logger.warning(f"Exception when sending mail {e}")
