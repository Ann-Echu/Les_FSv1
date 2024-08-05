import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

def get_google_auth():
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
    scope = "openid email profile"
    
    return OAuth2Session(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)

def login():
    google = get_google_auth()
    authorization_url, state = google.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )
    st.session_state['oauth_state'] = state
    st.write(f'<a href="{authorization_url}" target="_self">Login with Google</a>', unsafe_allow_html=True)

def logout():
    if 'oauth_token' in st.session_state:
        del st.session_state['oauth_token']
    st.session_state['logged_in'] = False

def callback():
    google = get_google_auth()
    
    if 'state' not in st.query_params or 'code' not in st.query_params:
        st.error("OAuth callback failed: Missing parameters")
        return None

    # Debugging step: Print the state values
    st.write(f"Expected state: {st.session_state.get('oauth_state')}")
    st.write(f"Received state: {st.query_params['state']}")

    if st.query_params['state'] != st.session_state.get('oauth_state'):
        st.error("OAuth callback failed: State mismatch")
        return None

    try:
        token = google.fetch_token(
            "https://oauth2.googleapis.com/token",
            grant_type="authorization_code",
            code=st.query_params['code']
        )
        st.session_state['oauth_token'] = token
        user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()
        return user_info
    except Exception as e:
        st.error(f"OAuth callback failed: {str(e)}")
        return None
