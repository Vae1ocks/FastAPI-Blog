import smtplib
from celery import shared_task


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
        except smtplib.SMTPRecipientsRefused:
            pass
        except Exception as e:  # noqa
            ...  # TODO: Logging
