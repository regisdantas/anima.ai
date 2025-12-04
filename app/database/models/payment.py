from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Payment:
    id: UUID | None
    user_id: UUID
    telegram_id: str
    payment_id: str
    credits: int
    status: str
    created_at: datetime | None = None
