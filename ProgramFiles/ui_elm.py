import streamlit as st
from .users import User, Admin
import pickle
from .databasemanager import DatabaseManager
import random

class UIelm:
    def __init__(self):
        st.title("Trackmint")
        st.session_state["login"] = False
        self.d = DatabaseManager()

    def get_all_data(self):
        f = open(r"./SystemFiles/passwords.dat", "rb")
        data = []
        while True:
            try:
                data.append(pickle.load(f))
            except EOFError:
                break
        return data


    def register(self): ### TO BE FIXED ###

        type = st.selectbox("Select User Type: ", ["Admin", "Resident"])

        if type == "Admin":


            new_username = st.text_input("Enter Community ID: ")
            new_pass1 = st.text_input("Enter Password: ", type="password")
            new_pass2 = st.text_input("Enter Password again: ", type="password")

            if new_username in self.d.get_all_keys():
                st.warning("Community already exists. Please log in.")

            if new_pass2 == new_pass1:
                if st.button("Register"):
                    st.success("Successfully registered.")
                    details = {new_username: {"Code": new_pass1, "Type": type}}
                    with open(r"./SystemFiles/passwords.dat", "ab") as f:
                        pickle.dump(details, f)

                    adm = Admin()
                    adm.create_main_table(new_username)
                    st.success("Successfully registered as {}".format(new_username))

        else:

            cID = st.text_input("Enter Community ID: ")
            building_name = st.text_input("Enter Apartment Number: ")
            new_pass1 = st.text_input("Enter Password: ", type="password")
            new_pass2 = st.text_input("Enter Password again: ", type="password")
            types = Admin().get_apt_types(cID)
            apt_type = st.selectbox("Types Menu", types)

            if st.button("Register"):

                if cID in self.d.get_all_keys():
                    
                    if new_pass2 == new_pass1:
                        
                        details = {cID+'r': {"AptN": building_name, "Code": new_pass1, "Type": type, "AptType":apt_type}}
                        with open(r"./SystemFiles/passwords.dat", "ab") as f:
                            pickle.dump(details, f)
                        info = {"Name":building_name, "ResidentID":cID, "Type":apt_type}
                        Admin().create_resident_table(cID, info)
                        st.success("Successfully registered.")

                    else:
                        st.warning("Re-enter details. Passwords do not match.")

                    st.info("Please login to continue.")

                else:
                    st.warning("Admin has not joined Trackmint.")

    def admin_controls(self, ID, CODE):
        col1, col2 = st.columns(2)
        usr = Admin()

        with col1:
            admn_choice = st.selectbox("Admin Menu", ["Add Rental Information", "Update Rental information", "Bills"])
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

            elif admn_choice == "Bills":
                
                bill_choices = ["Add Rent", "Change Rent", "Change Status", "Change Deadline", "View Bills"]

                bill_choice = st.radio("Choose task: ", bill_choices)

                if bill_choice == "Add Rent":
                    info = {}
                    names = usr.get_apt_names(ID)
                    if names:
                        name = st.selectbox("Choose Apartment Name", usr.get_apt_names(ID))
                        type = Admin().get_apt_type(ID, name)
                        st.text("You may choose to use the default values for the rent according to the Apartment Type.")
                        default = st.radio("Use Default Values?", ["Yes", "No"])[0]
                        if default == "Y":
                            info["DL"] = st.date_input("Enter Due Date (YYYY-MM-DD): ")
                            info["Status"] = st.radio("Has the amount been paid?", ["Y", "N"])
                            info["Rent"] = self.d.query("select RentalInformation from admn_rent_{} WHERE ApartmentType LIKE '{}'".format(ID, type))[0][0]
                        else:
                            info["Rent"] = st.text_input("Enter rent value: ")
                            info["DL"] = st.date_input("Enter Due Date (YYYY-MM-DD): ")
                            info["Status"] = st.radio("Has the amount been paid?", ["Y", "N"])
                        
                        info["AptNum"] = name
                        info["RentID"] = random.randint(1000, 10000)
                        info["Type"] = type
                        
                        if st.button("Confirm"):
                            usr.add_rent(ID, name, info)
                            st.success("Added Rent successfully.")

                elif bill_choice == "Change Rent":
                    info = {}
                    name = st.selectbox("Choose Apartment Name", usr.get_apt_names(ID))
                    info["RentID"] = st.text_input("Enter Rent ID:")
                    info["Rent"] = st.text_input("Enter rent value: ")
                    if st.button("Confirm"):
                        usr.change_rent(ID, info)

                    with col2:
                        st.text("Current Rent Information for {}:".format(name))
                        st.table(usr.get_rent_info(ID))

                elif bill_choice == "Change Deadline":
                    info = {}
                    name = st.selectbox("Choose Apartment Name", usr.get_apt_names(ID))
                    info["RentID"] = st.text_input("Enter Rent ID:")
                    info["Deadline"] = st.date_input("Enter New Due Date (YYYY-MM-DD): ")
                    if st.button("Confirm"):
                        usr.change_deadline(ID, info)

                    with col2:
                        st.text("Current Rent Information for {}:".format(name))
                        st.table(usr.get_rent_info(ID))

                elif bill_choice == "Change Status":
                    info = {}
                    name = st.selectbox("Choose Apartment Name", usr.get_apt_names(ID))
                    info["RentID"] = st.text_input("Enter Rent ID:")
                    info["Status"] = st.radio("Has the amount been paid?", ["Y", "N"])
                    if st.button("Confirm"):
                        usr.change_status(ID, info)
                        st.success("Values updated.")

                    with col2:
                        st.text("Current Rent Information for {}:".format(name))
                        st.table(usr.get_rent_info(ID))

                elif bill_choice == "View Bills":
                    name = st.selectbox("Choose Apartment Name", usr.get_apt_names(ID))
                    if st.button("Confirm"):
                        st.table(usr.get_rent_info(ID))

                else:
                    pass

            else:
                st.text("coming soon")

        with col2:
            st.text("Apartment Type And Rent: ")
            st.table(usr.get_main_table(ID))

    def resident_controls(self, ID, Apt, CODE):
        usr = User()

        data = Admin().get_apt_names(ID)

        col1, col2 = st.columns(2)

        with col1:

            if Apt not in data:
                info = {}
                info["Name"] = st.text_input("Enter Your Building Number: ")
                types = Admin().get_apt_types(ID)
                info["Type"] = st.selectbox("Types Menu", types)
                info["ResidentID"] = ID

                if st.button("Confirm"):
                    usr.create_resident_table(Apt, ID, info)
                    st.success("Created table for {}".format(ID))

            else:
                st.info("Table already exists. Please continue to tasks.")


                usr_choices = ["View Bills"]
                usr_choice = st.selectbox("Choose Task", usr_choices)

                if usr_choice == "View Bills":
                    st.table(usr.get_rent_info(ID, Apt))

                elif usr_choice == "Contact Admin":

                    st.text("coming soon.")

                else: 
                    pass

            with col2:

                st.write(
                        """
                        <style>
                        [data-testid="stMetricDelta"] svg {
                            display: none;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                rent_sum = self.d.query("Select SUM(Rent) from resn_{} GROUP BY Status HAVING Status = 'N'".format(ID))
                if len(rent_sum) != 0:
                    total_due = "Rs." + str(rent_sum[0][0])
                    due_by = "Due By: "+str(self.d.query("Select Deadline from resn_{} ORDER BY Deadline DESC".format(ID))[0][0])
                    st.metric("Total Due (Rs.)", total_due, due_by)
                else:
                    st.text("No Rent records found.")
        

    def login(self):

        user_type = st.sidebar.selectbox("User Type", ["Admin", "Resident"])

        if user_type == "Admin":
            
            ID = st.sidebar.text_input("Enter Community ID: ")
            CODE = st.sidebar.text_input("Enter Password: ", type="password")

            if st.sidebar.checkbox("Login"):
                if CODE == self.d.get_key_code(ID)[1]:
                    self.admin_controls(ID, CODE)

                else:
                    st.warning("Incorrect login details.")

        else:

            ID = st.sidebar.text_input("Enter Community ID:")
            Apt = st.sidebar.text_input("Enter Apartment Number: ")
            CODE = st.sidebar.text_input("Enter Password: ", type="password")

            if st.sidebar.checkbox("Login"):
                if CODE == self.d.get_resident_key_code(Apt, ID + 'r'):
                    self.resident_controls(ID, Apt, CODE)

                else:
                    st.warning("Incorrect login details.")