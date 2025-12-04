class HistoryRecord:
    def __init__(
        self,
        id,
        user_id,
        telegram_id,
        message_type,
        content,
        created_at,
    ):
        self.id = id
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.message_type = message_type
        self.content = content
        self.created_at = created_at
