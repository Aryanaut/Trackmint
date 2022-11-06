import streamlit as st
import mysql.connector as msq
from ProgramFiles.ui_elm import UIelm
from ProgramFiles.users import User, Admin
from ProgramFiles.databasemanager import DatabaseManager
import pickle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

u = UIelm()
d = DatabaseManager()

def main():
    menu = ["Home", "Login", "Register"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login")
        u.login()
        
    elif choice == "Register":
        st.subheader("Register")
        u.register()
        

if __name__ == "__main__":
    main()