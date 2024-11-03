import os
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def prospective_partner_page():

    if ("jwt" in st.session_state.keys()):
        token = st.session_state['jwt']
    else:
        st.session_state.jwt = {}
        
    st.title("Prospective Partner Application")

    st.write(
        "We are excited to explore potential partnerships! "
        "Please provide a brief paragraph explaining why you want to partner with us."
    )

    # Text input for the application
    application_text = st.text_area("Your Partnership Application", height=200)

    if st.button("Submit Application"):
        if application_text:
            # Here you would normally save the application to a database or send it via email
            # For this example, we will just display a success message
            st.success("Thank you for your application! We will review it and get back to you soon.")
            # Optionally display the submitted application
            st.write("Your application text:")
            st.write(application_text)
        else:
            st.error("Please enter a paragraph explaining your partnership interest.")

    def get_user_info(token):
        url = f"https://{AUTH0_DOMAIN}/userinfo"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)

        # Debugging output
        #st.write("User Info Response Code:", response.status_code)
        #st.write("User Info Response Body:", response.json())


        if response.status_code == 200:
            return response.json()
        else:
            st.write("Failed to retrieve user information.")
            return None


    jasonlol = get_user_info(token)

    responseCheck = (
        supabase_client.table("partner_applications")
        .select("*")
        .eq("uid", jasonlol["sub"])
        .execute()
    )
    #st.write(responseCheck)

    if (responseCheck.data == []):
        response = (
            supabase_client.table("partner_applications")
            .insert({"uid": jasonlol["sub"], "application": application_text})
            .execute()
        )

# Run the application page
prospective_partner_page()
