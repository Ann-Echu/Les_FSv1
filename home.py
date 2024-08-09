import streamlit as st
# from auth.google_auth import callback
def main():
    st.header('Les Fashion Secrets')
    st.divider()
    st.markdown("""
    🎉 Hello Fashion Enthusiasts! 🎉
    We are excited to introduce Les Fashion Secrets—your ultimate destination for personalized outfit recommendations tailored to your unique style. 
    As we test our algorithm, we’re using Valentine's Day as our theme, and we need your help to ensure it works perfectly!
    
    💌 Why Participate? Your input will help us fine-tune our algorithm, ensuring we provide accurate and personalized outfit recommendations based on your preferences, 
    using Valentine's Day as our focus. By sharing your style secrets, you’ll be part of a community that shapes the future of fashion.
    
    🔒 Your Privacy Matters Rest assured, your data will be kept safe and anonymous. 
    We value your trust and are committed to protecting your privacy every step of the way.
                
    👉 Fill Out Our Quick Survey Please take a few minutes to complete our survey. 
    Your insights are invaluable to us and will help us make Les Fashion Secrets better for everyone!
    
    Thank you for being a part of Les Fashion Secrets. Together, let’s make this Valentine’s Day and every day unforgettable! ❤️
    
    Warm regards,
    The Les Fashion Secrets Team
    """)
    st.write("About you!\nYour information is highly confidential, the following information is for internal research purpose only, all information will not be shared externally.")
    

# TODO: Include a link to the survey from homepage and
def fix_main():
    # Initialize the session state for page
    if 'page' not in st.session_state:
        st.session_state.page = "Main"

    # Navigation logic based on session state
    if st.session_state.page == "Main":
        st.header('Les Fashion Secrets')
        st.divider()
        st.markdown("""
        Hi everyone! Thanks for taking part in our survey.
        You're helping us out big time – our academic lives depend on it, quite literally!
        Anyway, this is a brief survey that should only take about 6 minutes of your time.
        We're collecting data on your fashion preferences and choices to help us build a machine
        for our Business Intelligence Project. Thank you again for your time.
        """)
        st.write("About you!\nYour information is highly confidential, the following information is for internal research purpose only, all information will not be shared externally.")

        # Button to navigate to recommendations
        if st.button("Go to Recommendations"):
            st.session_state.page = "Recommendation"
            st.experimental_rerun()

    elif st.session_state.page == "Recommendation":
        # recommendation_main()
        pass
