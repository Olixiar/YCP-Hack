# My first app
"""
Here's our first attempt at using data to create a table:
"""

import os

import streamlit as st
from supabase import create_client, Client

# Load environment variables
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
AUTH0_CALLBACK_URL = st.secrets["AUTH0_CALLBACK_URL"]

# Apply page configuration and hide the sidebar
st.set_page_config(initial_sidebar_state="collapsed")
token = st.session_state['jwt']

def sign_in():
    login_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=token&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&scope=openid profile email"
    
    if st.button("Sign In"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}" />', unsafe_allow_html=True)

def log_out():
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo={AUTH0_CALLBACK_URL}"
    
    if st.button("Log Out"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={logout_url}" />', unsafe_allow_html=True)


sign_in()
log_out()