from app.database.connectors.postgres import query_one, query, execute
from app.database.models.payment import Payment


def create_payment(payment: Payment) -> Payment | None:
    execute(
        """
        INSERT INTO payments (user_id, telegram_id, payment_id, credits, status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            str(payment.user_id),
            str(payment.telegram_id),
            payment.payment_id,
            payment.credits,
            payment.status,
        ),
    )

    return get_payment_by_payment_id(payment.payment_id)


def get_payment_by_telegram_id(telegram_id: str) -> list[Payment]:
    rows = query(
        """
        SELECT id, user_id, telegram_id, payment_id, credits, status, created_at
        FROM payments
        WHERE telegram_id = %s
        ORDER BY created_at DESC
        """,
        (str(telegram_id),),
    )

    return [
        Payment(
            id=row[0],
            user_id=row[1],
            telegram_id=row[2],
            payment_id=row[3],
            credits=row[4],
            status=row[5],
            created_at=row[6],
        )
        for row in rows
    ]


def get_payment_pending_by_telegram_id(telegram_id: str) -> list[Payment]:
    rows = query(
        """
        SELECT id, user_id, telegram_id, payment_id, credits, status, created_at
        FROM payments
        WHERE telegram_id = %s
        AND status = 'pending'
        ORDER BY created_at DESC
        """,
        (str(telegram_id),),
    )

    return [
        Payment(
            id=row[0],
            user_id=row[1],
            telegram_id=row[2],
            payment_id=row[3],
            credits=row[4],
            status=row[5],
            created_at=row[6],
        )
        for row in rows
    ]


def get_payment_by_payment_id(payment_id: str) -> Payment | None:
    row = query_one(
        """
        SELECT id, user_id, telegram_id, payment_id, credits, status, created_at
        FROM payments
        WHERE payment_id = %s
        """,
        (str(payment_id),),
    )

    if not row:
        return None

    return Payment(
        id=row[0],
        user_id=row[1],
        telegram_id=row[2],
        payment_id=row[3],
        credits=row[4],
        status=row[5],
        created_at=row[6],
    )


def update_payment_status(payment_id: str, new_status: str):
    execute(
        """
        UPDATE payments
        SET status = %s
        WHERE payment_id = %s
        """,
        (new_status, str(payment_id)),
    )


def update_payment(payment: Payment) -> Payment | None:
    execute(
        """
        UPDATE payments
        SET
            user_id = %s,
            telegram_id = %s,
            credits = %s,
            status = %s
        WHERE payment_id = %s
        """,
        (
            str(payment.user_id),
            str(payment.telegram_id),
            payment.credits,
            payment.status,
            str(payment.payment_id),
        ),
    )

    return get_payment_by_payment_id(payment.payment_id)
