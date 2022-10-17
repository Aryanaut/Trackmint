import streamlit as st
import streamlit_authenticator as auth
import yaml


with open("pass.yaml") as f:
    config = yaml.safe_load(f)

authenticator = auth.Authenticate(
    config['credentials'],
    config['cookie']['name']
    config['cookie']['key']
    config['cookie']['expiry_days']
    config['preauthorized']
)

name, status, username = authenticator.login("Login", "main")