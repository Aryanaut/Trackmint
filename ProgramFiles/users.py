from .databasemanager import DatabaseManager
import pandas as pd

class User:
    def __init__(self): 
        self.m = DatabaseManager()
        self.tables = []
        
        for table in self.m.query("Show tables"):
            if table[0][0:4] == "user":
                self.tables.append(table[0])

    def create_resident_table(self, TableName, ID, info):

        rent = self.m.query("select RentalInformation from admn_rent_{} WHERE ApartmentType LIKE '{}'".format(ID, info["Type"]))[0][0]

        query = "create table if not exists resn_"+TableName+" \
            (Name varchar(30) not null default '{}',\
            ResidentID int default '{}',\
            Rent int not null default {},\
            Deadline date, \
            Type varchar(30) not null default '{}' \
            PaidInTime char(1) default 'Y')".format(info["Name"], info["ResidentID"], rent, info["Type"])

        self.m.query(query)
        print("Table "+TableName+" created successfully!")

    def get_rent_info(self, TableName):
        query = "Select Rent, Deadline, PaidInTime from resn_{} ORDER BY Deadline".format(TableName)
        return pd.DataFrame(self.m.query(query), columns=["Rent", "Deadline", "PaidInTime"])


class Admin:
    def __init__(self):
        self.m = DatabaseManager()
        self.tables = []
        for table in self.m.query("Show tables"):
                self.tables.append(table[0])

    def create_main_table(self, TableName):

        query = "create table if not exists admn_rent_{} \
            (ApartmentType varchar(20) primary key,\
            RentalInformation int not null)".format(TableName)

        print("Table "+TableName+" created successfully!")
        self.m.query(query)

    def get_apt_names(self):

        query = "Show Tables"

        apt_list = self.m.query(query)
        out_list = []
        for row in apt_list:
            if row[0][:5] == "resn_":
                name = row[0][5:]
                out_list.append(name.title())

        return out_list

    def get_tables(self):

        query = "Show Tables"
        t_list = self.m.query(query)
        out_list = []
        for row in t_list:
            out_list.append(row[0])

        return out_list

    def get_apt_types(self, TableName):

        query = "Select ApartmentType from admn_rent_{}".format(TableName)

        apt_types = self.m.query(query)
        out_list = []
        for row in apt_types:
            out_list.append(row[0].title())

        return out_list

    def get_main_table(self, TableName):
        query = "Select * from admn_rent_{}".format(TableName)
        data = pd.DataFrame(self.m.query(query), columns=["Apartment Type", "Rent (Per Month)"])

        return data

    def update_main_table(self, TableName, info):
        for apt_type in info.keys():
            val = info[apt_type]
            query = "insert into admn_rent_{} values('{}',{})".format(TableName, apt_type, val)
            self.m.query(query)
            self.m.commit()
            print("Data entered and saved successfully!")

    def add_rent(self, TableName, info):
        query = "Insert Into resn_{}(Rent, Deadline, PaidInTime) Values({}, '{}', '{}')".format(TableName, info["Rent"], info["DL"], info["Status"])
        self.m.query(query)
        self.m.commit()
        print(query)

    def change_rent(self, TableName, info):
        query = "Update resn_{} SET Rent = {} WHERE Deadline = '{}'".format(TableName, info["Rent"], info["Deadline"])
        self.m.query(query)
        self.m.commit()

    def change_status(self, TableName, info):
        query = "Update resn_{} SET PaidInTime = '{}' WHERE Deadline = '{}'".format(TableName, info["Status"], info["Deadline"])
        self.m.query(query)
        self.m.commit()
        

    def change_deadline(self, TableName, info):
        query = "Update resn_{} SET Deadline = '{}' WHERE Deadline = '{}'".format(TableName, info["Deadline"], info["OldDeadline"])
        self.m.query(query)
        self.m.commit()

    def get_rent_info(self, TableName):
        query = "Select Rent, Deadline, PaidInTime from resn_{} ORDER BY Deadline".format(TableName)
        return pd.DataFrame(self.m.query(query), columns=["Rent", "Deadline", "PaidInTime"])