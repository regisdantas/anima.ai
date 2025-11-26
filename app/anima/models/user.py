import uuid

class User:
    def __init__(self, user_uuid: str = None, name: str = "", telegram_id:str = None):
        self._uuid = user_uuid if user_uuid else str(uuid.uuid4())
        self.name = name
        self.telegram_id = telegram_id
    
    @property
    def uuid(self):
        return self._uuid
