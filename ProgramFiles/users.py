from databasemanager import DatabaseManager

class User:
    def __init__(self):
        self.m = DatabaseManager()
        self.tables = []
        
        for table in self.m.query("Show tables"):
            if table[0][0:4] == "user":
                self.tables.append(table[0])

class Admin:
    def __init__(self):
        self.m = DatabaseManager()
        self.tables = []
        for table in self.m.query("Show tables"):
                self.tables.append(table[0])
