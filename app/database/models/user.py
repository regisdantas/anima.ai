import uuid
import hashlib
from datetime import datetime, timezone
from app.config.constants import ADMIN_TELEGRAM_ID_HASH


class User:
    def __init__(
        self,
        user_uuid: str = None,
        name: str = None,
        telegram_id: str = None,
        credit_balance: int = None,
        created_at: str = None,
        silence: bool = False,
    ):
        self._uuid = user_uuid if user_uuid else str(uuid.uuid4())
        self._name = name or "Unknown Name"
        self._telegram_id = telegram_id or "-1"
        self._credit_balance = credit_balance or 0
        self._silence = silence or False
        self._created_at = created_at or datetime.now(timezone.utc)

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def telegram_id(self):
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id):
        self._telegram_id = telegram_id

    @property
    def credit_balance(self):
        return self._credit_balance

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def silence(self):
        return self._silence

    @silence.setter
    def silence(self, silence):
        self._silence = silence


def check_admin(user: User) -> bool:
    user_hash = hashlib.md5(str(user.telegram_id).encode()).hexdigest()
    return user_hash == ADMIN_TELEGRAM_ID_HASH
