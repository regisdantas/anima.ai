from app.database.connectors.postgres import query_one, query, execute
from app.database.models.history import HistoryRecord


def create_history(
    user_id: str,
    telegram_id: str,
    message_type: str,
    content: str,
) -> HistoryRecord | None:
    execute(
        """
        INSERT INTO history (user_id, telegram_id, message_type, content)
        VALUES (%s, %s, %s, %s)
        """,
        (str(user_id), str(telegram_id), message_type, content),
    )

    return get_last_history_by_telegram_id(telegram_id)


def get_last_history_by_telegram_id(telegram_id: str) -> HistoryRecord | None:
    row = query_one(
        """
        SELECT id, user_id, telegram_id, message_type, content, created_at
        FROM history
        WHERE telegram_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (str(telegram_id),),
    )

    if not row:
        return None

    return HistoryRecord(
        id=row[0],
        user_id=row[1],
        telegram_id=row[2],
        message_type=row[3],
        content=row[4],
        created_at=row[5],
    )


def get_history_by_telegram_id(telegram_id: str, count: int = 1) -> list[HistoryRecord]:
    rows = query(
        """
        SELECT id, user_id, telegram_id, message_type, content, created_at
        FROM history
        WHERE telegram_id = %s
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (
            str(telegram_id),
            str(count),
        ),
    )

    return [
        HistoryRecord(
            id=row[0],
            user_id=row[1],
            telegram_id=row[2],
            message_type=row[3],
            content=row[4],
            created_at=row[5],
        )
        for row in rows
    ]


def delete_history_by_user_id(user_id: str):
    execute(
        """
        DELETE FROM history
        WHERE user_id = %s
        """,
        (str(user_id),),
    )


def delete_history_by_telegram(telegram_id: str):
    execute(
        """
        DELETE FROM history
        WHERE telegram_id = %s
        """,
        (str(telegram_id),),
    )
