import os
import streamlit as st

# Load environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# Apply page configuration and hide the sidebar
st.set_page_config(initial_sidebar_state="collapsed")

def sign_in():
    # Construct the Auth0 login URL
    login_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=token&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&scope=openid profile email"
    
    # Create a button to log in
    if st.button("Sign In"):
        # Redirect to Auth0 login page
        st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}" />', unsafe_allow_html=True)

def log_out():
    # Construct the Auth0 logout URL
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo={AUTH0_CALLBACK_URL}"
    
    # Create a button to log out
    if st.button("Log Out"):
        # Redirect to Auth0 logout page
        st.markdown(f'<meta http-equiv="refresh" content="0; url={logout_url}" />', unsafe_allow_html=True)

# Call the sign_in and log_out functions
sign_in()
log_out()