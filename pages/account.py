import streamlit as st
import requests
import os

# Environment Variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# Function to get user info from Auth0
def get_user_info(token):
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    # Debugging output
    st.write("User Info Response Code:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        st.write("Failed to retrieve user information:", response.status_code)
        st.write("Response body:", response.text)
        return None

st.write("Account Information")

# Get token from session state
token = st.session_state.get('jwt')

# Debug: Print the token value
st.write("Token Value:", token)

# Ensure token exists and is not empty
if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        st.write("User Info:", user_info)
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account!")
