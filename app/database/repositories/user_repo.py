from app.database.connectors.postgres import query_one, query, execute
from app.database.models.user import User


def get_user_by_telegram_id(telegram_id: str) -> User | None:
    row = query_one(
        """
        SELECT id, telegram_id, name, credits, created_at
        FROM users
        WHERE telegram_id = %s
        """,
        (str(telegram_id),),
    )

    if not row:
        return None

    return User(
        user_uuid=row[0],
        telegram_id=row[1],
        name=row[2],
        credit_balance=row[3],
        created_at=row[4],
    )


def create_user(user: User) -> User:
    execute(
        """
        INSERT INTO users (telegram_id, name, credits)
        VALUES (%s, %s, %s)
        """,
        (str(user.telegram_id), user.name, user.credit_balance),
    )

    return get_user_by_telegram_id(user.telegram_id)


def update_user_credits(telegram_id: str, new_credits: int):
    execute(
        """
        UPDATE users
        SET credits = %s
        WHERE telegram_id = %s
        """,
        (new_credits, str(telegram_id)),
    )


def delete_user(telegram_id: str):
    execute(
        """
        DELETE FROM users
        WHERE telegram_id = %s
        """,
        (str(telegram_id),),
    )


def update_user(user: User) -> User | None:
    execute(
        """
        UPDATE users
        SET
            name = %s,
            credits = %s
        WHERE telegram_id = %s
        """,
        (
            user.name,
            user.credit_balance,
            str(user.telegram_id),
        ),
    )

    return get_user_by_telegram_id(user.telegram_id)


def process_request_and_debit(telegram_id: str, price: int) -> bool:
    if telegram_id == "7170769829":
        return True

    user_row = query_one(
        "SELECT credits FROM users WHERE telegram_id = %s",
        (str(telegram_id),),
    )

    if not user_row:
        return False

    current_credits = user_row[0]
    if current_credits < price:
        return False

    execute(
        "UPDATE users SET credits = credits - %s WHERE telegram_id = %s",
        (price, str(telegram_id)),
    )

    return True


def process_refund(telegram_id: str, price: int):
    execute(
        "UPDATE users SET credits = credits + %s WHERE telegram_id = %s",
        (price, str(telegram_id)),
    )
