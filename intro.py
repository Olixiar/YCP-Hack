"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from config import apply_page_config, hide_default_sidebar

# Apply page configuration and hide the sidebar
apply_page_config()
hide_default_sidebar()

info = ("Hi")

if st.button("Sign Up"):
    st.switch_page("pages/meet.py")

info