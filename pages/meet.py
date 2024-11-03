import os
import requests
from dotenv import load_dotenv
from supabase import create_client
import streamlit as st


# Load environment variables for Supabase
load_dotenv()
SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

# Function to fetch posts from the database
def fetch_posts():
    # Query the "posts" table
    response = supabase_client.table("posts").select("title", "body", "uid").execute()
        
    return response.data  # Return the list of posts

def fetch_user(uid):
    user_response = supabase_client.table("users").select("name, bio", "email").eq("uid", uid).execute()
    
    return user_response.data[0]

def meet_page():
    st.title("Meet Page")
    st.write("Here are the latest posts from the community:")

    posts = fetch_posts()
    
    if posts:
        for post in posts:
            # Fetch user details for each post's user ID (uid)
            user = fetch_user(post["uid"])
            
            # Display the post with the user's name and bio below the body
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 20px; background-color: #f9f9f9;">
                    <h3>{post['title']}</h3>
                    <p>{post['body']}</p>
                    <hr style="margin: 10px 0;">
                    <p><strong>{user['name']}</strong></p>
                    <p style="color: #666; font-size: 14px;">{user['bio']}</p>
                    <p style="color: #666; font-size: 14px;">{user['email']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No posts available. Be the first to create a post!")

token = st.session_state.get("jwt")

if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        meet_page()
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account or login in order to use this feature!")