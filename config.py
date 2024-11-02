import streamlit as st

def apply_page_config():
    # Set the initial sidebar state to "collapsed"
    st.set_page_config(initial_sidebar_state="collapsed")

def hide_default_sidebar():
    # CSS to hide the default Streamlit sidebar for all pages
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