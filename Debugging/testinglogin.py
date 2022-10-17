from matplotlib.style import available
import streamlit as st
import mysql.connector as msq

connector = msq.connect(username="root", password="sql123", host="localhost", database="wilson")
cursor = connector.cursor()
resi = {101:'abc', 102:'acf', 103:'ggh', 104:'hhg'}

username = int(input("Enter usercode: "))
password = input("Enter password: ")

adnpass = '1234566'

def query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def check_permissions(username, passwd):
    if username in resi:
        if passwd == resi[username]:
            return True, 0
        else:
            return False, None
    else:
        if passwd == adnpass:
            return True, 1
        else:
            return False, None

status, mode = check_permissions(username, password)

if status == False:
    print("False.")
else:
    availableList = query("Show Tables;")
    if mode == 0:
        print("Available tables:")
        for i in availableList:
            if i[0][0:4] == "user":
                print(i[0])
    else:
        print("Available tables:")
        for i in availableList:
            print(i[0])


