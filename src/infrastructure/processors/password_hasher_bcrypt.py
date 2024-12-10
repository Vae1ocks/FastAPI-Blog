from typing import NewType

import bcrypt
import hashlib
import base64
import hmac

from application.processors.password_hasher import PasswordHasher
from infrastructure.types import PasswordPepper


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, pepper: PasswordPepper):
        self.pepper = pepper

    def hash(self, raw_password: str) -> bytes:
        base64_hmac_password: bytes = self.add_pepper(
            raw_password,
            self.pepper,
        )
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(base64_hmac_password, salt)

    @staticmethod
    def add_pepper(raw_password: str, pepper: str) -> bytes:
        hmac_password: bytes = hmac.new(
            key=pepper.encode(),
            msg=raw_password.encode(),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(hmac_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        base64_hmac_password: bytes = self.add_pepper(
            raw_password=raw_password,
            pepper=self.pepper,
        )
        return bcrypt.checkpw(base64_hmac_password, hashed_password.encode())
