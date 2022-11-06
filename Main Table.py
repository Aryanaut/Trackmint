import mysql.connector

def create_database_main_table():
    global db
    db = input("Enter the name of your database - ")

    mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = 'aryan')
    mycursor = mydb.cursor()

    query = "create database if not exists %s" % (db,)
    mycursor.execute(query)
    print()
    print()
    print("Your database has been created successfully!")
    print()
    print()
    mycursor = mydb.cursor()
    mycursor.execute("Use "+db)
    
    global TableName
    TableName = input("Enter the name of the table - ")
    print()

    query = "create table if not exists "+TableName+" \
        (ApartmentType varchar(20) primary key,\
         RentalInformation int not null)"

    print("Table "+TableName+" created successfully!")
    mycursor.execute(query)
    print()

def input_data_main_table():
    while True:
        mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = 'aryan')
        mycursor = mydb.cursor()
        mycursor.execute("Use "+db)
        AptType = input("Specify your housing type - ")
        RentInfo = input("Specify the rent information for the above selected/chosen housing type - ")
        print()
        query = "insert into TableName values('{}','{}')".format(AptType, RentInfo)
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        print("Data entered and saved successfully!")
        print()
        ch = input("Do you want to insert more data records ? (y/n)")
        if ch == "n":
            break



inp = int(input("Enter any integer to start the program and 0 to terminate it - "))
print()

if inp == 0:
    print("Program Terminating...")
    print()

while inp!=0:
    print("1. Enter 1 to create your database and the main table for the FMS")
    print()
    print("2. Enter 2 to add records in the table created")
    print()
    
    ch = int(input("Enter your choice based on the above options - "))
    print()

    if ch == 1:
        create_database_main_table()

    elif ch == 2:
        input_data_main_table()

    else:
        print("Invalid Statement, not recognised!")
        break

