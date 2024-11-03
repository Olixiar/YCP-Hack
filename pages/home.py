import streamlit as st
import requests
import os
from streamlit_url_fragment import get_fragment
from supabase import create_client

# Environment Variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

st.set_page_config(layout="wide")
st.image("./assets/cover.png", width=1425)

# Initialize session state for token
if 'jwt' not in st.session_state:
    st.session_state['jwt'] = None

# Get the token from URL fragment
current_value = get_fragment()
if current_value and "access_token=" in current_value:
    token = current_value.split("access_token=")[1].split("&")[0]
    st.session_state['jwt'] = token

# Get token from session state
token = st.session_state['jwt']

# Debug: Print the token value
st.write("Token Value:", token)

# Ensure token exists and is not empty
if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        st.write("User Info:", user_info)

        # Initialize Supabase client and perform actions
        SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co"
        SUPABASE_KEY = "your_supabase_key"  # Keep this secret in a real app
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

        response_check = supabase_client.table("users").select("*").eq("uid", user_info["sub"]).execute()
        if not response_check.data:
            response = supabase_client.table("users").insert({
                "uid": user_info["sub"],
                "role": "Student",
                "first_name": "Gabe",
                "last_name": "Baitinger"
            }).execute()
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account!")

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
