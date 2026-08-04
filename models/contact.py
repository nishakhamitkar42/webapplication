import logging
from database.db import get_db_connection

logger = logging.getLogger(__name__)

class Contact:
    def __init__(self, name, email, subject, message, id=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.created_at = created_at

    def save(self):
        """Save the contact submission to the SQLite database."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
                (self.name, self.email, self.subject, self.message)
            )
            conn.commit()
            self.id = cursor.lastrowid
            logger.info(f"Contact saved with ID: {self.id}")
            return self.id
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to save contact: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """Retrieve all contact form submissions from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            subject=row['subject'],
            message=row['message'],
            created_at=row['created_at']
        ) for row in rows]
