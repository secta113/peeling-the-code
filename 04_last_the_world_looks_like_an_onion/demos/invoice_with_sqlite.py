import sqlite3


def save(order_id: str, total: int) -> None:
    with sqlite3.connect("prod.db") as conn:
        conn.execute("INSERT INTO invoices VALUES (?, ?)", (order_id, total))
