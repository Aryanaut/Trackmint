import mysql.connector as msq
import pickle

class DatabaseManager:
    def __init__(self):
        self.connector = msq.connect(user="root", passwd="sql123", host="localhost", database="wilson")
        self.cursor = self.connector.cursor()

    def query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.connector.commit()

    def get_all_data(self):
        f = open(r"./SystemFiles/passwords.dat", "rb")
        data = {}
        while True:
            try:
                data.update(pickle.load(f))
            except EOFError:
                break
        return data