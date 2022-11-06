import streamlit as st
from .users import User, Admin
import pickle
from .databasemanager import DatabaseManager

class UIelm:
    def __init__(self):
        st.title("Trackmint")
        st.session_state["login"] = False
        self.d = DatabaseManager()

    def get_all_data(self):
        f = open(r"./SystemFiles/passwords.dat", "rb")
        data = {}
        while True:
            try:
                data.update(pickle.load(f))
            except EOFError:
                break
        return data


    def register(self):

        type = st.selectbox("Select User Type: ", ["Admin", "Resident"])
        new_username = st.text_input("Enter Community ID: ")
        new_pass1 = st.text_input("Enter Password: ")
        new_pass2 = st.text_input("Enter Password again: ")
        building_name = st.text_input("Enter Apartment Name: ")

        if st.button("Register"):
            
            if new_username in self.get_all_data().keys():
                st.warning("User already exists. Please log in.")

            else:

                if new_pass2 == new_pass1:
                    st.success("Successfully registered.")
                    details = {new_username: {"Code": new_pass1, "Type": type, "Apt":building_name}}
                    with open(r"./SystemFiles/passwords.dat", "ab") as f:
                        pickle.dump(details, f)

                    if type == "Admin":
                        adm = Admin()
                        adm.create_main_table(building_name)
                        st.success("Successfully registered as {}".format(building_name))

                    else:
                        usr = User()
                        apt_name = st.text_input("Enter Apartment Number: ")
                        usr.create_resident_table(apt_name)
                        st.success("Successfully registered as {}".format())

                    st.info("Please login to continue.")


                else:
                    st.warning("Re-enter details. Passwords do not match.")

    def login(self):

        ID = st.sidebar.text_input("Enter Community ID: ")
        CODE = st.sidebar.text_input("Enter Code: ", type="password")

        if st.sidebar.checkbox("Login"):
            data = self.get_all_data()
            print(data)
            if CODE == data[ID]["Code"]:

                ### If User is logged in ###

                st.subheader("Dashboard")

                if data[ID]["Type"] == "Admin": ### Admin Controls ###

                    col1, col2 = st.columns(2)
                    usr = Admin()

                    with col1:
                        admn_choice = st.selectbox("Admin Menu", ["Add Rental Information", "Update Rental information", "Track Bills", "Messages"])
                        if admn_choice == "Add Rental Information":
                            ### Current Rental information being added ###

                                if "admn_rent_{}".format(ID) not in usr.get_tables():
                                    usr.create_main_table(ID)
                                    st.success("Created Rent Table for {}".format(ID))

                                else:
                                    st.info("Table for {} exists.".format(ID))

                                num_type = st.text_input("Enter Number of Apartment Types: ")
                                rent = {}

                                if num_type != "":

                                    for i in range(int(num_type)):
                                        apt_type = st.text_input("Apartment Type: ", key=1+i)
                                        val = st.text_input("Rent (Per Month): ", key=2+i)
                                        if st.button("Confirm", key=i+3):
                                            rent[apt_type] = val

                                usr.update_main_table(ID, rent)

                        elif admn_choice == "Update Rental information":
                            
                            types = usr.get_apt_types(ID)
                            apt_type = st.selectbox("Types Menu", types)
                            new_rent = st.text_input("Enter New Rent: ")

                            if st.button("Confirm"):
                                self.d.query("Update admn_rent_{} SET RentalInformation = {} Where ApartmentType = '{}'".format(ID, new_rent, apt_type))
                                self.d.commit()
                                st.success("Information Updated.")

                        elif admn_choice == "Track Bills":
                            st.text("coming soon")

                        else:
                            st.text("coming soon")

                    with col2:
                        st.table(usr.get_main_table(ID))
                            
                else: ### User Controls ###
                    usr = User()

            else:

                ### If login fails ###

                st.warning("Incorrect Username or Password.")


