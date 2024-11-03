import streamlit as st
import requests
import os
import streamlit as st
from supabase import create_client, Client

# Environment Variables
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
AUTH0_CALLBACK_URL = st.secrets["AUTH0_CALLBACK_URL"]


SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


st.markdown("<h1 style='color: darkgreen;'>Account Information</h1>", unsafe_allow_html=True)

# Function to get user info from Auth0
def get_user_info(token):
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    # Debugging output
    #st.write("User Info Response Code:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        st.write("Failed to retrieve user information:", response.status_code)
        st.write("Response body:", response.text)
        return None


def submit_profile_page():
    st.write("Please fill out your profile information below.")

    # Role selection using radio buttons
    role = st.radio("Select Your Role:", ("Staff", "Student", "Partner"))

    # Text inputs for additional profile information
    name = st.text_input("Your Name")
    bio = st.text_area("A brief bio about yourself", height=200)
    
    # Process submission
    if st.button("Submit Profile"):
        if name and bio:
            # Retrieve user information
            token = st.session_state.get("jwt")
            user_info = get_user_info(token)

            if user_info:
                uid = user_info["sub"]

                # Insert profile data into Supabase
                response = (
                    supabase_client.table("users") 
                    .update({"name": name, "role": role, "bio": bio})
                    .eq("uid", uid)
                    .execute()
                )

                if response.data:
                    st.success("Profile submitted successfully!")
                else:
                    st.error("Failed to submit your profile.")
                    st.write("Error details:", response.get("error_message", "No error message provided."))
            else:
                st.error("Could not verify user information.")
        else:
            st.error("Please fill in all fields before submitting.")


# Get token from session state
token = st.session_state.get('jwt')

# Debug: Print the token value
#st.write("Token Value:", token)

# Ensure token exists and is not empty
if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        #st.write("User Info:", user_info)
        submit_profile_page()
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account or login in order to use this feature!")
