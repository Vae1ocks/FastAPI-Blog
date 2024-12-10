from abc import ABC, abstractmethod


class MailSender(ABC):
    @abstractmethod
    def send(self, email: str, subject: str, message: str): ...
