# db.py
#!/usr/bin/env python3
import sqlite3

DB_NAME = "database.db"

def connect_to_db():
    return sqlite3.connect(DB_NAME)

def create_db_table():
    conn = None
    try:
        conn = connect_to_db()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name    TEXT NOT NULL,
                email   TEXT NOT NULL,
                phone   TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
            """
        )
        conn.commit()
        print("User table ensured/created successfully")
    except Exception as e:
        print(f"User table creation failed: {e}")
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id: int):
    user, conn = {}, None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"],
            }
    except Exception as e:
        print(f"get_user_by_id error: {e}")
    finally:
        if conn:
            conn.close()
    return user

def get_users():
    users, conn = [], None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        for r in cur.fetchall():
            users.append({
                "user_id": r["user_id"],
                "name": r["name"],
                "email": r["email"],
                "phone": r["phone"],
                "address": r["address"],
                "country": r["country"],
            })
    except Exception as e:
        print(f"get_users error: {e}")
    finally:
        if conn:
            conn.close()
    return users

def insert_user(user: dict):
    inserted_user, conn = {}, None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (name, email, phone, address, country)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user["name"], user["email"], user["phone"], user["address"], user["country"])
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        if conn: conn.rollback()
        print(f"insert_user error: {e}")
    finally:
        if conn: conn.close()
    return inserted_user

def update_user(user: dict):
    updated_user, conn = {}, None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE users
               SET name = ?, email = ?, phone = ?, address = ?, country = ?
             WHERE user_id = ?
            """,
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        if conn: conn.rollback()
        print(f"update_user error: {e}")
    finally:
        if conn: conn.close()
    return updated_user

def delete_user(user_id: int):
    message, conn = {"status": "Cannot delete user"}, None
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        if conn: conn.rollback()
        print(f"delete_user error: {e}")
    finally:
        if conn: conn.close()
    return message
