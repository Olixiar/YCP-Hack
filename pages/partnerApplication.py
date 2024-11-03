import os
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()
SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
st.markdown("<h1 style='color: darkgreen;'>Prospective Partner Application</h1>", unsafe_allow_html=True)

# Function to retrieve user info from Auth0
def get_user_info(token):
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.write("Failed to retrieve user information:", response.status_code)
        st.write("Response body:", response.text)
        return None

# Page for prospective partners
def prospective_partner_page():
    st.write(
        "We are excited to explore potential partnerships! "
        "Please provide a brief paragraph explaining why you want to partner with us."
    )

    # Text input for the application
    application_text = st.text_area("Your Partnership Application", height=200)

    # Process submission
    if st.button("Submit Application"):
        if application_text:
            # Retrieve user information
            token = st.session_state.get("jwt")
            user_info = get_user_info(token)

            if user_info:
                uid = user_info["sub"]

                # Check if the user already has an application
                response_check = (
                    supabase_client.table("partner_applications")
                    .select("*")
                    .eq("uid", uid)
                    .execute()
                )

                # Only insert if no previous application exists
                if response_check.data == []:
                    response = (
                        supabase_client.table("partner_applications")
                        .insert({"uid": uid, "application": application_text})
                        .execute()
                    )
                    if response.data:
                        st.success("Thank you for your application! We will review it and get back to you soon.")
                    else:
                        st.error("Failed to submit your application.")
                        st.write("Error details:", response.get("error_message", "No error message provided."))
                else:
                    st.info("You have already submitted an application.")
            else:
                st.error("Could not verify user information.")
        else:
            st.error("Please enter a paragraph explaining your partnership interest.")

# Main section to check if user is authenticated
token = st.session_state.get("jwt")

if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        prospective_partner_page()
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account or login in order to use this feature!")
