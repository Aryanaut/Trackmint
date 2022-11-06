import mysql.connector as msq

class DatabaseManager:
    def __init__(self):
        self.connector = msq.connect(username="root", password="infinity2022", host="localhost", database="wilson")
        self.cursor = self.connector.cursor()

    def query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.connector.commit()