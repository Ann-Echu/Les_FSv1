import streamlit as st
from streamlit_option_menu import option_menu
from home import main as home_main
from about import main as about_main
from recommendation import main as recommendation_main
from auth.google_auth import login, callback, logout

#TODO: fix login for invalid redirect_uri_mismatch error
# # Function to handle login
# def login_page():
#     st.sidebar.title("Login")
#     login()

# # Function to handle logout
# def logout_page():
#     logout()
#     st.sidebar.success("Logged out successfully!")
#     st.session_state['logged_in'] = False

# Main Application
def run():
    # Create Web-page Layout
    st.set_page_config(layout="wide",
                       page_title="Les Fashion secrets",
                       page_icon="🛍️")

    # Main application
    # if 'logged_in' not in st.session_state:
    #     st.session_state['logged_in'] = False

    # Handle the callback and add oauth_token to session state
    # if 'oauth_token' not in st.session_state and 'code' in st.query_params:
    #     user_info = callback()
    #     if user_info:
    #         st.session_state['logged_in'] = True
    #         st.session_state['email'] = user_info['email']
    #     else:
    #         st.error("Login failed. Please try again.")

    # if st.session_state.logged_in:
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as {st.session_state['email']}")
    st.sidebar.button("Logout", on_click=logout_page)
    page = st.sidebar.selectbox("Go to", ["Home", "About", "Recommendation"])

    if page == "Home":
        home_main()
    elif page == "About":
        about_main()
    elif page == "Recommendation":
        recommendation_main()
    # else:
    #     login_page()

if __name__ == "__main__":
    run()
