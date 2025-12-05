from app.database.connectors.postgres import query_one, query, execute
from app.database.models.user import User, check_admin


def get_all_users() -> list[User]:
    rows = query(
        """
        SELECT id, telegram_id, name, credits, created_at
        FROM users
        """
    )

    users = []
    for row in rows:
        users.append(
            User(
                user_uuid=row[0],
                telegram_id=row[1],
                name=row[2],
                credit_balance=row[3],
                created_at=row[4],
            )
        )

    return users


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


def update_user_credits(user: User, new_credits: int):
    execute(
        """
        UPDATE users
        SET credits = %s
        WHERE telegram_id = %s
        """,
        (new_credits, str(user.telegram_id)),
    )


def delete_user(user: User):
    execute(
        """
        DELETE FROM users
        WHERE telegram_id = %s
        """,
        (str(user.telegram_id),),
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


def process_request_and_debit(user: User, price: int) -> bool:
    if check_admin(user):
        return True

    user_row = query_one(
        "SELECT credits FROM users WHERE telegram_id = %s",
        (str(user.telegram_id),),
    )

    if not user_row:
        return False

    current_credits = user_row[0]
    if current_credits < price:
        return False

    execute(
        "UPDATE users SET credits = credits - %s WHERE telegram_id = %s",
        (price, str(user.telegram_id)),
    )

    return True


def process_refund(user: User, price: int):
    execute(
        "UPDATE users SET credits = credits + %s WHERE telegram_id = %s",
        (price, str(user.telegram_id)),
    )
