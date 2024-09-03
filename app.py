import streamlit as st
from database.db_handler import insert_user, find_user_by_email, check_password, hash_password
from home import main as home_main
from about import main as about_main
from recommendation import main as recommendation_main
from contactus import main as contact_main
from privacy import main as privacy_main
from utils import login_page, registration_page  # Import from utils.py

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.query_params.clear()  # Clear the URL query params
    st.rerun()

def require_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to access this page.")
        login_page()
        st.stop()

def run():
    st.set_page_config(layout="wide",
                       page_title="Les Fashion Secrets",
                       page_icon="🛍️")

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = "Home"  # Default page is 'Home'

    st.sidebar.image("static/images/logo1.png", use_column_width=True)
    
    query_params = st.query_params  # Retrieve query params
    page = query_params.get('page', "Home") # Default to 'Home' if no 'page' parameter is present
    
    if st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as {st.session_state['user']['username']}")
        if st.sidebar.button("Logout"):
            logout()
    # else:
        # if page == "Survey":
        #     st.warning("You need to log in to access the Survey page.")
        #     login_page()
        #     st.stop()
    
    # Reset the URL by clearing query params when changing the page
    def navigate_to(selected_page):
        st.query_params.update(page=selected_page)
        st.session_state['page'] = selected_page  # Update the session state with the new page

    page = st.sidebar.selectbox(
        "Navigate to", 
        ["Home", "Survey", "Contact Us", "Privacy", "Register", "Login"],
        index=["Home", "Survey", "Contact Us", "Privacy", "Register", "Login"].index(page),
        on_change=lambda: navigate_to(st.session_state["page"])
    )

    # Set the page content based on the selected page
    if page == "Home":
        home_main()
    elif page == "About":
        about_main()
    elif page == "Survey":
        recommendation_main()
    elif page == "Contact Us":
        contact_main()
    elif page == "Privacy":
        privacy_main()
    elif page == "Register":
        registration_page()
    elif page == "Login":
        login_page()

if __name__ == "__main__":
    run()
