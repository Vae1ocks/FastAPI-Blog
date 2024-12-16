from abc import ABC, abstractmethod


class MailSender(ABC):
    @abstractmethod
    def send(self, targets: list[str], subject: str, message: str): ...
