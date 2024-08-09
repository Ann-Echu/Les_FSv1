import streamlit as st
import pandas as pd
from collections import defaultdict
import random
import numpy as np
from database.db_handler import insert_survey_response

# Helper function to handle and display multiboxes.
def select_items(item_list, prefix):
    selected_items = []
    for idx, item in enumerate(item_list):
        if st.checkbox(item, key=f"{prefix}_{idx}"):
            selected_items.append(item)
    return selected_items

def __recommender(name):
    user_preferences_df = pd.read_csv('responses.csv')
    outfits_df = pd.read_csv('final_outfit_characteristics.csv')

    # Ensure both dataframes have the same columns before concatenating
    if list(user_preferences_df.columns) != list(outfits_df.columns):
        raise ValueError("The columns of user preferences and outfits dataframes do not match.")

    # Convert all columns to strings to ensure uniform data type
    user_preferences_df = user_preferences_df.astype(str)
    outfits_df = outfits_df.astype(str)

    # Define a threshold for matching characteristics
    threshold = 11  # At least 11 matching characteristics out of 16

    def hasMatch(userValue, outfitValue):
        if type(userValue) != str or type(outfitValue) != str:
            return False
        
        userValue = getSplitAttributes(userValue)
        outfitValue = getSplitAttributes(outfitValue)
        return len(userValue.intersection(outfitValue)) > 0

    def getSplitAttributes(values):
        return set([v.strip() for v in values.split(";")])

    user_outfit_matches = []
    matchedOutfits = defaultdict(list)
    outfitAttributes = set(outfits_df.columns.values)
    outfitAttributes.remove("ID")

    for userIndex, user in user_preferences_df.iterrows():
        userGender = user['Gender']
        
        for outfitIndex, outfitData in outfits_df.iterrows():
            if outfitData['Gender'] != userGender:
                continue
            
            matchedAttributeCt = 0
            
            for attribute in outfitAttributes:
                outfitAttrData = outfitData[attribute]
                userAttrData = user[attribute]
                
                if hasMatch(outfitAttrData, userAttrData):
                    matchedAttributeCt += 1
            
            if matchedAttributeCt >= threshold:
                matchedOutfits[userIndex].append(outfitData["ID"])
        
        matchedOutfitCt = len(matchedOutfits[userIndex])

    table_data = []
    for userIndex in sorted(matchedOutfits.keys()):
        table_data.append([f"{name}", f"{len(matchedOutfits[userIndex])} matched outfits"])

    st.write(table_data)

def main():
    st.header('Les Fashion Secrets')
    st.divider()
    st.markdown("""
    Hi everyone!
                
    Thank you for being a part of Les Fashion Secrets. Together, let’s make this Valentine’s Day and every day unforgettable! ❤️
    """)
    st.write("About you!\nYour information is highly confidential, the following information is for internal research purpose only, all information will not be shared externally.")
    st.divider()
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Retrieve email and username directly from the session state    
    email = st.session_state['user']['email']
    name = st.session_state['user']['name']

    def next_step():
        st.session_state.step += 1

    def prev_step():
        st.session_state.step -= 1

    def reset_steps():
        st.session_state.step = 0

    total_steps = 6
    current_step = st.session_state.step
    progress = (current_step + 1) / total_steps
    st.progress(progress)

    # Step 1: Basic Information
    if st.session_state.step == 0:
        with st.container():
            st.subheader("Step 1: Basic Information")
            st.write("*Please select your gender:")
            gender = st.radio(
                "Choose one:",
                ('Woman','Man','Non-binary','Prefer not to say','Other')
            )
            if gender == 'Other':
                other_gender = st.text_input("Please specify:")
                gender = other_gender if other_gender else gender

            st.write("*How old are you?")
            age = st.radio(
                "Choose one:",
                ('Under 18: Youth','18-24: Young Adult','25-34: Adult','35-44: Mid Adult','45-54: Senior Adult','55 or over: Senior')
            )

            if gender and age:
                if st.button("Next"):
                    st.session_state.responses['Gender'] = gender
                    st.session_state.responses['Age'] = age
                    next_step()

    # Step 2: Valentine's Day Questions
    elif st.session_state.step == 1:
        with st.container():
            st.subheader("Step 2: Valentine's Day Questions")
            
            st.write("*What is your current relationship status?")
            relationship_status = st.radio(
                "Choose one:",
                ['Single', 'In a relationship', 'Married', 'Divorced', 'Widowed', 'Other']
            )
            if relationship_status == 'Other':
                other_status = st.text_input("Please specify:")
                relationship_status = other_status if other_status else relationship_status

            st.write("*What are your plans for Valentine's Day? (Select all that apply)")
            valentines_plans_list = ['Dinner date', 'Casual outing', 'Romantic getaway', 'Staying in', 'Other']
            valentines_plans = select_items(valentines_plans_list, "valentines_plans")

            st.write("*What’s the weather like during Valentine’s Day?")
            valentines_weather = st.radio(
                "Choose one:",
                ['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy', 'Stormy', 'Other']
            )
            if valentines_weather == 'Other':
                other_weather = st.text_input("Please specify:")
                valentines_weather = other_weather if other_weather else valentines_weather

            st.write("*Do you have a preference for certain types of outfits for Valentine’s Day? (Select all that apply)")
            valentines_outfits_list = ['Elegant/Formal', 'Casual/Comfortable', 'Trendy/Fashion-forward', 'Romantic/Sexy', 'Laidback/Comfy']
            valentines_outfits = select_items(valentines_outfits_list, "valentines_outfits")

            st.write("*Which colors would you prefer to wear for Valentine's Day? (Select all that apply)")
            valentines_colors_list = ['Red', 'Pink', 'White', 'Black', 'Other colors', 'No color preference']
            valentines_colors = select_items(valentines_colors_list, "valentines_colors")

            if relationship_status and valentines_plans and valentines_weather and valentines_outfits and valentines_colors:
                if st.button("Next"):
                    st.session_state.responses['Relationship_Status'] = relationship_status
                    st.session_state.responses['Valentines_Plans'] = valentines_plans
                    st.session_state.responses['Valentines_Weather'] = valentines_weather
                    st.session_state.responses['Valentines_Outfits'] = valentines_outfits
                    st.session_state.responses['Valentines_Colors'] = valentines_colors
                    next_step()

            if st.button("Previous"):
                prev_step()

    # Step 3: Work and Weather Preferences
    elif st.session_state.step == 2:
        with st.container():
            st.subheader("Step 3: Work and Weather Preferences")
            
            st.write("*What type of outfits do you typically wear for work? ")
            typical_outfits_list = [
                'Corporate (e.g., suits, formal attire)',
                'Semi-Formal (e.g., dress shirts, slacks, skirts)', 
                'Casual (e.g., jeans, casual tops)', 
                'Uniform (e.g., scrubs, specific work attire)',
                'Other (Please specify)'
            ]
            typical_outfits = select_items(typical_outfits_list, "typical_outfits")

            st.write("*What is the weather like where you are? ")
            weather_list =['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy', 'Stormy']
            weather = select_items(weather_list, "weather")

            if typical_outfits and weather:
                if st.button("Next"):
                    st.session_state.responses['Work_Attire'] = typical_outfits
                    st.session_state.responses['Weather'] = weather
                    next_step()

            if st.button("Previous"):
                prev_step()

    # Step 4: Fashion Profile
    elif st.session_state.step == 3:
        with st.container():
            st.subheader("Step 4: Fashion Profile")
            st.markdown("This is where we get to know your fashion choices as an individual")
            st.write("In a month,")
            date_outfits_frequency = st.radio(
                "How often do you wear date nights/night outs outfits?",
                ['Rarely', 'Sometimes', 'Often', 'Never'],
                horizontal=True
            )

            casual_frequency = st.radio(
                "How often do you wear casual outfits?",
                ['Rarely', 'Sometimes', 'Often', 'Never'],
                horizontal=True
            )

            work_outfits_frequency = st.radio(
                "How often do you wear outfits for work?",
                ['Rarely', 'Sometimes', 'Often', 'Never'],
                horizontal=True
            )

            st.write("What styles do you prefer from the options below? (Select all that apply)")
            styles_list = [
                'Grungy', 'Sexy', 'Casual', 'Laidback/Comfy', 'Classy', 'Showy', 'Colorful',
                'Formal', 'Bohemian', 'Streetwear', 'All of the above'
            ]
            styles = select_items(styles_list, "styles")

            if date_outfits_frequency and casual_frequency and work_outfits_frequency and styles:
                if st.button("Next"):
                    st.session_state.responses['Date_Outfits_Frequency'] = date_outfits_frequency
                    st.session_state.responses['Casual_Frequency'] = casual_frequency
                    st.session_state.responses['Work_Outfits_Frequency'] = work_outfits_frequency
                    st.session_state.responses['Preferred_Styles'] = styles
                    next_step()

            if st.button("Previous"):
                prev_step()

    # Step 5: Fit and Style Preferences
    elif st.session_state.step == 4:
        with st.container():
            st.subheader("Step 5: Fit and Style Preferences")

            st.write("Which type of bottoms do you prefer?")
            bottoms_list = ['Trousers', 'Shorts', 'Skirts', 'Other']
            bottoms = select_items(bottoms_list, "bottoms")

            st.write("Which type of tops do you prefer?")
            tops_list = ['T-shirts', 'Sweaters', 'Sweatshirts', 'Tanks', 'Other']
            tops = select_items(tops_list, "tops")

            st.write("Which type of shoes do you buy most often?")
            shoes_list = ['Sneakers', 'Boots', 'Sandals', 'Flats', 'Heels', 'Other']
            shoes = select_items(shoes_list, "shoes")

            st.write("What colors do you prefer for your clothes? (Select all that apply)")
            colors_list = [
                'Neutrals and Basics (Beiges, Black, Grays, White, Navy, Browns)',
                'Brights and Bold Colors (Reds, Oranges, Yellows, Greens, Blues)',
                'Soft and Pastel Colors (Pinks, Purples, Teal)',
                'Metallics and Special Colors (Gold, Silver, Burgundy)',
                'Other (Please specify)'
            ]
            colors = select_items(colors_list, "colors")

            st.write("Do you like your clothes loose or fitted?")
            fit_preferences_list = ['Loose', 'Fitted', 'Top Fitted, Bottom Loose', 'Bottom Fitted, Top Loose']
            fit_preferences = select_items(fit_preferences_list, "fit_preferences")

            st.write("Please select the option that best describes your silhouette:")
            silhouette_list = [
                'Hourglass', 'Apple/Round', 'Pear', 'Rectangle/Straight', 'Inverted Triangle', 'Oval/Circle', 'Athletic/Rectangle'
            ]
            silhouette = st.radio(
                "Silhouette:",
                silhouette_list
            )

            if bottoms and tops and shoes and colors and fit_preferences and silhouette:
                if st.button("Submit"):
                    st.session_state.responses['Bottom_Type'] = bottoms
                    st.session_state.responses['Top_Type'] = tops
                    st.session_state.responses['Shoe_Type'] = shoes
                    st.session_state.responses['Colors'] = colors
                    st.session_state.responses['Fit_Preferences'] = fit_preferences
                    st.session_state.responses['Silhouette'] = silhouette
                    ID = int(random.uniform(90, 1000))
                    st.session_state.responses.update({
                        'ID': ID,
                        'Email': email,
                        'Name': name
                    })

                    # Insert the response into the survey_collections
                    insert_survey_response(st.session_state.responses)

                    st.write("Form Submitted!")
                    reset_steps()

            if st.button("Previous"):
                prev_step()

if __name__ == '__main__':
    main()
