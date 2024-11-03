import os
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()
SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
def create_post_page():
    st.title("Create a New Post")

    # Input fields for post details
    post_title = st.text_input("Post Title")
    post_body = st.text_area("Post Body", height=200)

    if st.button("Submit Post"):
        if post_title and post_body:
            # Here you would normally save the post to a database
            # For this example, we display a success message and the post details
            token = st.session_state.get("jwt")
            user_info = get_user_info(token)
            uid = user_info["sub"]
            response = (
                supabase_client.table("posts")
                .insert({"uid": uid, "title": post_title, "body": post_body})
                .execute()
                )
            st.success("Post created successfully!")
            
            # Display the submitted post for verification
            st.write("### Post Details")
            st.write(f"**Title:** {post_title}")
            st.write(f"**Body:** {post_body}")
        else:
            st.error("Please fill out all fields before submitting.")

    
# Main section to check if user is authenticated
token = st.session_state.get("jwt")

if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        create_post_page()
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account or login in order to use this feature!")
