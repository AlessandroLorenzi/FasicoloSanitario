import sqlite3

class AnalisysRepository:
    def __init__(self, sqlite_path):
        sqlite3.register_converter("timestamp", self._convert_timestamp)
        self.connection = sqlite3.connect(
            sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS analisys (document TEXT, date TIMESTAMP, name TEXT, value TEXT, UNIQUE(document, name))"
        )
        cursor.close()

    def _convert_timestamp(self, val):
        val = val.decode("utf-8") 
        val = val.replace("T", " ") 
        return val

    def insert(self, document_id, date, name, value):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO analisys (document, date, name, value) VALUES (?, ?, ?, ?)",
                (document_id, date.isoformat(), name, value),
            )
            self.connection.commit()
            cursor.close()
        except sqlite3.IntegrityError:
            # If elaborate again the same file, the same values are already in the database
            pass

    def get_all_names(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT name FROM analisys")
        names = cursor.fetchall()
        cursor.close()
        return names

    def get_all_values_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT date, name, value FROM analisys WHERE name = ? ORDER BY DATE DESC", (name,))
        values = cursor.fetchall()
        cursor.close()
        return values
