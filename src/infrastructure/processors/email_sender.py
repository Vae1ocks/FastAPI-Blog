from dataclasses import dataclass

from application.processors.email_sender import MailSender
from infrastructure.celery.tasks import send_email

@dataclass(frozen=True)
class EmailSender(MailSender):
    host: str
    host_user: str
    host_password: str
    port: int


    def send(self, emails: list[str], subject: str, message: str) -> str:
        task = send_email.delay(
            host=self.host,
            host_user=self.host_user,
            host_password=self.host_password,
            port=self.port,
            emails=emails,
            subject=subject,
            message=message,
        )
        return task.id
