import sqlite3
from datetime import datetime
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "spammer_memory.db"


def initialize_memory():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Conversation history
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS conversations (
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                role TEXT NOT NULL,
                                                                content TEXT NOT NULL,
                                                                timestamp TEXT NOT NULL
                   )
                   """)

    # Permanent personal memories
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS personal_memory (
                                                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                  category TEXT NOT NULL,
                                                                  information TEXT NOT NULL,
                                                                  created_at TEXT NOT NULL
                   )
                   """)

    # Memory candidates awaiting approval
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS memory_candidates (
                                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    category TEXT NOT NULL,
                                                                    information TEXT NOT NULL,
                                                                    risk_level TEXT NOT NULL,
                                                                    status TEXT NOT NULL DEFAULT 'pending',
                                                                    created_at TEXT NOT NULL
                   )
                   """)

    connection.commit()
    connection.close()


def save_message(role, content):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (role, content, timestamp)
        VALUES (?, ?, ?)
        """,
        (role, content, datetime.now().isoformat())
    )

    connection.commit()
    connection.close()


def get_recent_messages(limit=20):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM conversations
        ORDER BY id DESC
            LIMIT ?
        """,
        (limit,)
    )

    messages = cursor.fetchall()
    connection.close()

    return [
        {"role": role, "content": content}
        for role, content in reversed(messages)
    ]


def save_memory(category, information):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO personal_memory
        (category, information, created_at)
        VALUES (?, ?, ?)
        """,
        (category, information, datetime.now().isoformat())
    )

    connection.commit()
    connection.close()


def get_all_memories():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category, information
        FROM personal_memory
        ORDER BY id ASC
        """
    )

    memories = cursor.fetchall()
    connection.close()

    return [
        {"category": category, "information": information}
        for category, information in memories
    ]
def save_memory_candidate(category, information, risk_level):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memory_candidates
            (category, information, risk_level, status, created_at)
        VALUES (?, ?, ?, 'pending', ?)
        """,
        (
            category,
            information,
            risk_level,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()

def get_pending_candidates():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, category, information, risk_level
        FROM memory_candidates
        WHERE status = 'pending'
        ORDER BY id ASC
        """
    )

    candidates = cursor.fetchall()
    connection.close()

    return [
        {
            "id": item[0],
            "category": item[1],
            "information": item[2],
            "risk_level": item[3]
        }
        for item in candidates
    ]

def approve_memory_candidate(candidate_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category, information
        FROM memory_candidates
        WHERE id = ? AND status = 'pending'
        """,
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    if candidate is None:
        connection.close()
        return False

    category, information = candidate

    # Check whether the memory already exists.
    cursor.execute(
        """
        SELECT 1
        FROM personal_memory
        WHERE LOWER(TRIM(category)) = LOWER(TRIM(?))
          AND LOWER(TRIM(information)) = LOWER(TRIM(?))
            LIMIT 1
        """,
        (category, information)
    )

    exists = cursor.fetchone() is not None

    if not exists:
        cursor.execute(
            """
            INSERT INTO personal_memory
                (category, information, created_at)
            VALUES (?, ?, ?)
            """,
            (category, information, datetime.now().isoformat())
        )

    cursor.execute(
        """
        UPDATE memory_candidates
        SET status = 'approved'
        WHERE id = ?
        """,
        (candidate_id,)
    )

    connection.commit()
    connection.close()

    return True

def reject_memory_candidate(candidate_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE memory_candidates
        SET status = 'rejected'
        WHERE id = ? AND status = 'pending'
        """,
        (candidate_id,)
    )

    rejected = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return rejected


def memory_exists(category, information):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM personal_memory
        WHERE LOWER(TRIM(category)) = LOWER(TRIM(?))
          AND LOWER(TRIM(information)) = LOWER(TRIM(?))
            LIMIT 1
        """,
        (category, information)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def candidate_exists(category, information):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM memory_candidates
        WHERE LOWER(TRIM(category)) = LOWER(TRIM(?))
          AND LOWER(TRIM(information)) = LOWER(TRIM(?))
          AND status = 'pending'
            LIMIT 1
        """,
        (category, information)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists

def delete_memory(memory_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM personal_memory
        WHERE id = ?
        """,
        (memory_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted

def get_memories_with_ids():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, category, information
        FROM personal_memory
        ORDER BY id ASC
        """
    )

    memories = cursor.fetchall()
    connection.close()

    return [
        {
            "id": item[0],
            "category": item[1],
            "information": item[2]
        }
        for item in memories
    ]