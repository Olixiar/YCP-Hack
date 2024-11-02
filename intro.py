"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from config import apply_page_config, hide_default_sidebar

# Apply page configuration and hide the sidebar

# --- PAGE SETUP ---
home = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/cottage:",
    default=True,
)
meet = st.Page(
    "pages/meet.py",
    title="Meet",
    icon=":material/groups:",
)
sign_in = st.Page(
    "pages/sign_up.py",
    title="Sign Up",
    icon=":material/login:",
)
sign_up = st.Page(
    "pages/sign_in.py",
    title="Sign In",
    icon=":material/how_to_reg:",
)
account = st.Page(
    "pages/account.py",
    title="Account",
    icon=":material/account_circle:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Navigation": [home, meet],
        "Account Manegment": [account, sign_in, sign_up],
    }
)