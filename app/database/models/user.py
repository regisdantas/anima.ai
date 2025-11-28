import uuid


class User:
    def __init__(self, user_uuid: str = None, name: str = "", telegram_id: str = None):
        self._uuid = user_uuid if user_uuid else str(uuid.uuid4())
        self.name = name
        self.telegram_id = telegram_id
        self._credit_balance = 0
        self._last_response = None

    @property
    def uuid(self):
        return self._uuid

    @property
    def credit_balance(self):
        return self._credit_balance

    def add_credits(self, amount: int):
        self._credit_balance += amount

    def deduct_credits(self, amount: int) -> bool:
        if amount > self._credit_balance:
            return False
        self._credit_balance -= amount
        return True

    def get_history(self) -> str:
        return ""

    @property
    def last_response(self):
        return self._last_response

    @last_response.setter
    def last_response(self, response):
        self._last_response = response
