import streamlit as st
from streamlit_option_menu import option_menu
from home import main as home_main
from about import main as about_main
from recommendation import main as recommendation_main
from auth.google_auth import login, callback, logout
# from user import login

import recommendation

import home
import about

# function to handle login
def login_page():
    st.sidebar.title("Login")
    login()

# Function to handle logout
def logout_page():
    logout()
    st.sidebar.title("Logged out successfully")

# Main Application
def run():
    # Create Web-page Layout
    st.set_page_config(layout="wide",
                        page_title="Les Fashion secrets",
                        page_icon="🛍️")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # TODO fix st.experimental_get_query_params() => st.query_params
    if 'oauth_token' not in st.session_state and 'code' in st.experimental_get_query_params():
        user_info = callback()
        st.session_state['logged_in'] = True
        st.session_state['email'] = user_info['email']
        st.session_state['oauth_token'] = user_info

    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        st.sidebar.write(f"Logged in as {st.session_state['email']}")
        st.sidebar.button("Logout", on_click=logout_page)
        # Create a horizontal menu for navigation between pages
        page = st.sidebar.selectbox("Go to", ["Home", "About", "Recommendation"])

        if page == "Home":
            home_main()
        elif page == "About":
            about_main()
        elif page == "Recommendation":
            recommendation_main()

    else:
        login_page()


if __name__ == "__main__":
    run()
