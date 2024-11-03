from openai import OpenAI
import streamlit as st

st.title("YCP Bot")

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
    #st.write("User Info Response Code:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        st.write("Failed to retrieve user information:", response.status_code)
        st.write("Response body:", response.text)
        return None

token = st.session_state.get('jwt')

if token and isinstance(token, str) and token.strip():
    user_info = get_user_info(token)
    if user_info:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
    else:
        st.write("Failed to retrieve user information.")
else:
    st.write("Make an account or login in order to use this feature!")
