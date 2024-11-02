"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

info = ("Hi")

if st.button("Sign Up"):
    st.switch_page("pages/meet.py")

info



st.markdown(
    """
    <style>
    /* Hide the multipage app sidebar */
    [data-testid="stAppViewContainer"] > div:first-child {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)