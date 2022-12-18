import mysql.connector as msq
import pickle

class DatabaseManager:
    def __init__(self):
        self.connector = msq.connect(user="root", passwd="infinity2022", host="localhost", database="wilson")
        self.cursor = self.connector.cursor()

    def query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.connector.commit()

    def get_all_data(self):
        f = open(r"./SystemFiles/passwords.dat", "rb")
        data = []
        while True:
            try:
                data.append(pickle.load(f))
            except EOFError:
                break
        return data

    def get_key_code(self, id):
        data = self.get_all_data()
        for record in data:
            if list(record.keys())[0] == id:
                return (id, record[list(record.keys())[0]]["Code"])

    def get_all_keys(self):
        data = self.get_all_data()
        keys = []
        for record in data:
            key = list(record.keys())[0]
            if record[key]["Type"] == "Admin":
                keys.append(key)

        return keys

    def get_resident_key_code(self, Apt, id):
        data = self.get_all_data()
        for record in data:
            key = list(record.keys())[0]
            if key == id:
                return record[key]["Code"]
                    