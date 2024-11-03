import os
from dotenv import load_dotenv
from supabase import create_client
import streamlit as st

# Load environment variables from .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to fetch partnership data from Supabase
def get_partnership_data():
    # Fetch data from the "partnerships" table
    response = supabase_client.table("partnerships").select("partner_name, image, description").execute()
    
    return response.data

# Get the data
data = get_partnership_data()

# Custom CSS for styling the display
st.markdown(
    """
    <style>
    .partnership-card {
        display: flex;
        flex-direction: column;
        align-items: center;  /* Center horizontally */
        justify-content: center; /* Center vertically */
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .partnership-logo {
        width: 100px;
        height: 100px;
        margin-bottom: 10px;
        border-radius: 8px;
        object-fit: cover;  /* Ensures the image covers the area without distortion */
    }
    .partnership-name {
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        text-align: center; /* Center text */
    }
    .partnership-description {
        font-size: 16px;
        text-align: center;
        margin-top: 10px;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display data in styled cards
for i in data:
    st.markdown(f"""
    <div class="partnership-card">
        <img class="partnership-logo" src="{i['image']}" alt="{i['partner_name']} logo">
        <h3 class="partnership-name">{i['partner_name']}</h3>
        <p class="partnership-description">{i['description']}</p>
    </div>
    """, unsafe_allow_html=True)