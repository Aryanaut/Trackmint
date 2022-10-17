import streamlit as st
import mysql.connector as msq

connector = msq.connector(user="root", host="localhost", password="sql123", database="wilson")
cursor = connector.cursor()

