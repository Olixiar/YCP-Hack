import os
import streamlit as st
from dotenv import load_dotenv

# Load Auth0 credentials from .env
load_dotenv()
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# Page Configuration and Sidebar Hiding
st.set_page_config(initial_sidebar_state="collapsed")

# JavaScript to extract access token from URL fragment
st.markdown("""
<script>
function getAccessToken() {
    const url = window.location.href;
    const tokenMatch = url.match(/access_token=([^&]+)/);
    if (tokenMatch) {
        const accessToken = tokenMatch[1];
        console.log('Access token found: ' + accessToken);  // Debug log
        // Redirect to the same page with the token as a query param
        window.location.replace(window.location.pathname + '?access_token=' + accessToken);
    } else {
        console.log('No access token found in the URL.');  // Debug log
    }
}

// Call the function to extract the token
getAccessToken();
</script>
""", unsafe_allow_html=True)

# Function to extract access token from the URL
def extract_access_token():
    query_params = st.query_params
    return query_params.get("access_token", [None])[0]

# Get access token from the URL
access_token = extract_access_token()

# Debug log for access token extraction
st.write("Extracted Access Token:", access_token)

# Set access token in session state
if access_token and "access_token" not in st.session_state:
    st.session_state["access_token"] = access_token
    st.experimental_rerun()  # Refresh to clear URL and display updated state

# Auth0 login, signup, and logout URLs
def get_auth0_url(action="login"):
    response_type = "token"
    return f"https://{AUTH0_DOMAIN}/{action}?client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&response_type={response_type}"

def get_logout_url():
    return f"https://{AUTH0_DOMAIN}/v2/logout?returnTo=http://localhost:8501&client_id={AUTH0_CLIENT_ID}"

# Display Title
st.title("Welcome to My App")

# Display the current URL in the console for debugging
st.markdown(f"<script>console.log('Current URL: {window.location.href}');</script>", unsafe_allow_html=True)

# Check for logged-in state
if "access_token" in st.session_state:
    st.write("Welcome back! You are signed in.")
    
    # Display Logout Button
    if st.button("Log Out"):
        logout_url = get_logout_url()
        st.markdown(f'<a href="{logout_url}" target="_self">Logout</a>', unsafe_allow_html=True)

    # Show the access token for debugging
    st.write(f"Your access token: {st.session_state['access_token']}")
else:
    st.write("Please Sign In or Sign Up to access more features.")

    # Display Login and Signup Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Sign In"):
            st.markdown(f"[Click here to Sign In]({get_auth0_url('authorize')})", unsafe_allow_html=True)
    with col2:
        if st.button("Sign Up"):
            st.markdown(f"[Click here to Sign Up]({get_auth0_url('signup')})", unsafe_allow_html=True)

# Debugging: Output current session state for troubleshooting
st.write("Current session state:", st.session_state)
