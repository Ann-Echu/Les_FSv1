import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os

def get_google_auth():
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
    scope = "openid email profile"

    return OAuth2Session(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

def login():
    google = get_google_auth()
    authorization_url, state = google.create_authorization_url("https://accounts.google.com/o/oauth2/auth")
    st.session_state['oauth_state'] = state
    st.write(f'<a href="{authorization_url}" target="_self">Login with Google</a>', unsafe_allow_html=True)

def callback():
    google = get_google_auth()
    # TODO fix st.experimental_get_query_params() => st.query_params
    token = google.fetch_token("https://oauth2.googleapis.com/token", authorization_response=st.experimental_get_query_params())
    user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()
    return user_info

def logout():
    if 'oauth_token' in st.session_state:
        del st.session_state['oauth_token']
    st.session_state['logged_in'] = False
