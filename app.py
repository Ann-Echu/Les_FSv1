import streamlit as st
import recommendation
from streamlit_option_menu import option_menu
import home
import about

def run():
    # Create Web-page Layout
    st.set_page_config(layout="wide",
                        page_title="Les Fashion secrets",
                        page_icon="🛍️")
    
    # Create a horizontal menu for navigation between pages
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", "About", "Outfits Recommender"], 
            icons=['house', 'info','dress'], menu_icon="cast", default_index=0)

    # Load the selected page script
    if selected == "Home":
        home.app()
    elif selected == "About":
        about.app()
    elif selected == "Outfits Recommender":
        recommendation.main()
        

if __name__ == "__main__":
    run()