# My first app
"""
Here's our first attempt at using data to create a table:
"""

import os
import streamlit as st
from streamlit_url_fragment import get_fragment

import supabase
import streamlit as st
from supabase import create_client, Client

# Load environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# Apply page configuration and hide the sidebar
st.set_page_config(initial_sidebar_state="collapsed")

def sign_in():
    login_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=token&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&scope=openid profile email"
    
    if st.button("Sign In"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}" />', unsafe_allow_html=True)

def log_out():
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo={AUTH0_CALLBACK_URL}"
    
    if st.button("Log Out"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={logout_url}" />', unsafe_allow_html=True)





current_value = get_fragment()
##Full Fragment from URL
#st.write(f"Full fragment value: {current_value!r}") 

if current_value and "access_token=" in current_value:
    token = current_value.split("access_token=")[1].split("&")[0]
    st.write("Access Token:")
    st.write(token)

    
    SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = (
        supabase_client.table("users")
        .insert({"jwt": token, "role": "Student", "first_name": "Gabe", "last_name": "Baitinger"})
        .execute()
    )

    st.session_state["jwt"] = token







sign_in()
log_out()