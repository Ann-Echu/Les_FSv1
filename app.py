import streamlit as st
from database.db_handler import insert_user, find_user_by_email, check_password, hash_password
from home import main as home_main
from about import main as about_main
from recommendation import main as recommendation_main
from contactus import main as contact_main
from privacy import main as privacy_main

def login_user(email, password):
    user = find_user_by_email(email)
    if user and check_password(password, user['password_hash']):
        return user
    else:
        return None

def registration_page():
    st.title("Register")
    name = st.text_input("Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Register"):
        if password == confirm_password:
            if find_user_by_email(email):
                st.error("Email already registered. Please login instead.")
            else:
                insert_user(email, name, username, password)
                st.success("Registration successful! You can now log in.")
                st.experimental_rerun()
        else:
            st.error("Passwords do not match")

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user'] = user
            st.success(f"Logged in as {user['username']}")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.experimental_rerun()

def require_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to access this page.")
        login_page()
        st.stop()

def run():
    st.set_page_config(layout="wide",
                       page_title="Les Fashion Secrets",
                       page_icon="🛍️")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    st.sidebar.image("static/images/logo1.png", use_column_width=True)
    
    if st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as {st.session_state['user']['username']}")
        if st.sidebar.button("Logout"):
            logout()
        page = st.sidebar.selectbox("Navigate to", ["Home", "About", "Recommendation", "Contact Us"])
    else:
        page = st.sidebar.selectbox("Navigate to", ["Home", "About", "Recommendation", "Contact Us", "Register", "Login"])

    if page == "Home":
        home_main()
    elif page == "About":
        about_main()
    elif page == "Recommendation":
        require_login()
        recommendation_main()
    elif page == "Contact Us":
        contact_main()
    elif page == "Register":
        registration_page()
    elif page == "Login":
        login_page()

if __name__ == "__main__":
    run()
