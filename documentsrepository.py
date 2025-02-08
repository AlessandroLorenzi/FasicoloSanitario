import sqlite3
import uuid

class DocumentsRepository:
    def __init__(self, sqlite_path):
        sqlite3.register_converter("timestamp", self._convert_timestamp)
        self.connection = sqlite3.connect(
            sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS documents (id text, date timestamp, prestazione text, filename text UNIQUE, content text) "
        )
        cursor.close()

    def _convert_timestamp(self, val):
        val = val.decode("utf-8") 
        val = val.replace("T", " ") 
        return val
    
    def insert(self, filename, date, prestazione, content):
        cursor = self.connection.cursor()
        id = uuid.uuid4().hex
        cursor.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?)",
            (id, date, prestazione, filename, content),
        )
        self.connection.commit()
        cursor.close()
        return id
    
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, date, prestazione, filename, content FROM documents")
        documents = cursor.fetchall()
        cursor.close()
        return documents

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, date, prestazione, filename, content FROM documents WHERE id = ?", (id,))
        document = cursor.fetchone()
        cursor.close()
        return document