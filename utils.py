import streamlit as st
from database.db_handler import *
import os
import pandas as pd

def login_user(email, password):
    user = find_user_by_email(email)
    if user and check_password(password, user['password_hash']):
        return user
    else:
        return None



def get_user_survey_response(user_id):
    return get_user_survey(user_id)  # Replace with actual function to get survey response from DB

def update_survey_response(user_id, responses):
    update_user_survey(user_id, responses)  # Replace with actual function to update survey response in DB

def insert_survey_response(responses):
    # Insert the survey response into the database
    # Assuming responses contain all necessary data
    insert_user_survey(responses)

def registration_page(email=None):
    st.title("Register")
    email = st.text_input("Email")
    name = st.text_input("Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Register"):
        if password == confirm_password:
            if find_user_by_email(email):
                st.error("Email already registered. Please login instead.")
            else:
                user_id = insert_user(email, name, username, hash_password(password))
                st.session_state['logged_in'] = True
                st.session_state['user'] = {'email': email, 'name': name, 'username': username}
                st.session_state['user_id'] = user_id  # Store the user ID in session state
                st.success("Registration successful! Your survey has been submitted.")
                st.rerun()  # Refresh the app state
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
            st.session_state['user_id'] = user['id']
            st.success(f"Logged in as {user['username']}")
            submit_survey_response()  # Automatically submit the survey response
            st.query_params.clear()  # Clear the URL query params
            st.rerun()  # Rerun the app after login to refresh the state
        else:
            st.error("Invalid email or password")

def submit_survey_response():
    """Submits the survey response to the database."""
    if 'responses' in st.session_state and 'user' in st.session_state:
        st.session_state.responses['Email'] = st.session_state['user']['email']
        st.session_state.responses['Name'] = st.session_state['user']['name']
        insert_survey_response(st.session_state.responses)
        save_to_csv(st.session_state.responses)
        st.success("Survey submitted successfully!")

def save_to_csv(response):
    file_path = 'data/survey_responses03.csv'
    df = pd.DataFrame([response])

    # Check if CSV exists
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)