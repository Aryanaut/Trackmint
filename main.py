import streamlit as st
import mysql.connector as msq
from ProgramFiles.ui_elm import UIelm
from ProgramFiles.users import User, Admin
from ProgramFiles.databasemanager import DatabaseManager
import pickle

u = UIelm()
d = DatabaseManager()

intro_text = """
            Trackmint is a platform that allows residencies and apartments to track their residents' rental information. \n
            To use Trackmint, a community's admin must register as an Admin through the Trackmint App with an __Admin ID__. After an admin is registered, users may use the __Admin ID__ to create their accounts on the app. \n
            Admins can add information about the community's apartment types and their respective rent values. Admins can also add rent records for different users, which the user will be able to see once they log in. \n
            Users, upon logging in, will be able to see how much they owe, their previous records of payment and the deadline for remanining payments. 
            Admins may also change rent records for different users upon request. 
            """

def main():
    menu = ["Home", "Login", "Register"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(intro_text)

    elif choice == "Login":
        st.subheader("Login")
        u.login()
        
    elif choice == "Register":
        st.subheader("Register")
        u.register()
        

if __name__ == "__main__":
    main()