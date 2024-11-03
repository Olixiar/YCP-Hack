import streamlit as st
st. set_page_config(layout="wide")
# --- HERO SECTION ---

import streamlit as st
from streamlit_url_fragment import get_fragment
import supabase
from supabase import create_client, Client
import requests
import os


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
SUPABASE_URL = "https://awlnmyhowvrfcravqihl.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bG5teWhvd3ZyZmNyYXZxaWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1Nzc3NDEsImV4cCI6MjA0NjE1Mzc0MX0.B8crTyUGLAjK1r-lzmLZezdExm2LTUmd7i54cYogGKQ"

st.image("./assets/cover.png", width=1425)

st.write("\n")
st.title("What We Do", anchor=False)
st.write("The Graham Center for Collaborative Innovation (GCCI) is dedicated to fostering cross-disciplinary exploration and creativity, serving as a central hub for collaboration across the York College of Pennsylvania, as well as its administrative and co-curricular units. At GCCI, we are committed to cultivating partnerships that transcend academic boundaries, connecting the university with the local business community while prioritizing student learning and engagement.")
st.write("With a rich history of joint projects, experiential learning, and resource sharing, GCCI actively promotes collaborative initiatives that not only highlight the talent and innovative spirit of York College of Pennsylvania (YCP) but also inspire future cooperative endeavors. As such, we have worked together to bring you YCPartner, allowing us to showcase these partnerships and creating opportunities for collaboration and success")

# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Goals", anchor=False)
st.write(
    """
    - Information Collection: Develop a user-friendly platform to gather information on existing YCP partnerships, both internal and external, allowing interested parties to easily search and learn about these collaborations.
    - Partnership Building: Create an accessible way for YCP faculty, students, staff, businesses, other colleges, and community organizations to express their interest in forming new partnerships.
    - Networking Opportunities: Implement features that facilitate connections between potential partners based on shared interests and goals, utilizing AI modeling for compatible collaborations.
    - Collaborative Ideation: Leverage AI technology to generate creative and mutually beneficial collaboration ideas tailored to the needs and objectives of potential partners.
    """
)

if ("jwt" in st.session_state.keys()):
    token = st.session_state['jwt']
else:
    st.session_state.jwt = {}

current_value = get_fragment()
##Full Fragment from URL
#st.write(f"Full fragment value: {current_value!r}") 

if current_value and "access_token=" in current_value:
    token = current_value.split("access_token=")[1].split("&")[0]
#    st.write("Access Token:")
#    st.write(token)
    st.session_state.jwt = token

    
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        supabase_client.table("users")
        .select("*")
        .eq("uid", jasonlol["sub"])
        .execute()
    )
    #st.write(responseCheck)
    
    if (responseCheck.data == []):
        response = (
            supabase_client.table("users")
            .insert({"uid": jasonlol["sub"], "role": "Placeholder Role", "name": "Placeholder Name", "email": jasonlol["email"]})
            .execute()
        )

#    st.write(st.session_state.jwt)
