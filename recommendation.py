import streamlit as st
import pandas as pd
from collections import defaultdict
import random
from utils import get_user_survey_response, update_survey_response, insert_survey_response, registration_page

class Survey:
    def __init__(self, user):
        self.user = user
        self.user_id = st.session_state.get('user_id')
        self.responses = {}
        self.step = 0
        self.total_steps = 6
        self.initialize_session_state()
        self.existing_response = get_user_survey_response(self.user_id)  # Check if the user has an existing survey response

    def initialize_session_state(self):
        if 'step' not in st.session_state:
            st.session_state.step = 0
        if 'responses' not in st.session_state:
            st.session_state.responses = {}

    def check_existing_response(self):
        if self.existing_response:
            st.warning("You have already submitted the survey.")
            if st.button("Refill and Overwrite Survey"):
                st.session_state.responses = self.existing_response  # Load existing responses if needed
                self.reset_steps()  # Restart the survey from the beginning
            else:
                st.stop()

    def select_items(self, item_list, prefix):
        selected_items = []
        for idx, item in enumerate(item_list):
            if st.checkbox(item, key=f"{prefix}_{idx}"):
                selected_items.append(item)
        return selected_items

    def next_step(self):
        st.session_state.step += 1

    def prev_step(self):
        st.session_state.step -= 1

    def reset_steps(self):
        st.session_state.step = 0

    def progress_bar(self):
        current_step = st.session_state.step
        progress = (current_step + 1) / self.total_steps
        st.progress(progress)

    def step_1_basic_information(self):
        st.subheader("Step 1: Basic Information")
        gender = st.radio("Choose one:", ('Woman', 'Man', 'Non-binary', 'Prefer not to say', 'Other'))
        if gender == 'Other':
            other_gender = st.text_input("Please specify:")
            gender = other_gender if other_gender else gender

        age = st.radio("Choose one:", ('Under 18: Youth', '18-24: Young Adult', '25-34: Adult', '35-44: Mid Adult', '45-54: Senior Adult', '55 or over: Senior'))

        if gender and age:
            if st.button("Next"):
                st.session_state.responses['Gender'] = gender
                st.session_state.responses['Age'] = age
                self.next_step()

    def step_2_valentines_day_questions(self):
        st.subheader("Step 2: Valentine's Day Questions")
        relationship_status = st.radio("Choose one:", ['Single', 'In a relationship', 'Married', 'Divorced', 'Widowed', 'Other'])
        if relationship_status == 'Other':
            other_status = st.text_input("Please specify:")
            relationship_status = other_status if other_status else relationship_status

        valentines_plans = self.select_items(['Dinner date', 'Casual outing', 'Romantic getaway', 'Staying in', 'Other'], "valentines_plans")
        valentines_weather = st.radio("Choose one:", ['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy', 'Stormy', 'Other'])
        if valentines_weather == 'Other':
            other_weather = st.text_input("Please specify:")
            valentines_weather = other_weather if other_weather else valentines_weather

        valentines_outfits = self.select_items(['Elegant/Formal', 'Casual/Comfortable', 'Trendy/Fashion-forward', 'Romantic/Sexy', 'Laidback/Comfy'], "valentines_outfits")
        valentines_colors = self.select_items(['Red', 'Pink', 'White', 'Black', 'Other colors', 'No color preference'], "valentines_colors")

        if relationship_status and valentines_plans and valentines_weather and valentines_outfits and valentines_colors:
            if st.button("Next"):
                st.session_state.responses['Relationship_Status'] = relationship_status
                st.session_state.responses['Valentines_Plans'] = valentines_plans
                st.session_state.responses['Valentines_Weather'] = valentines_weather
                st.session_state.responses['Valentines_Outfits'] = valentines_outfits
                st.session_state.responses['Valentines_Colors'] = valentines_colors
                self.next_step()

        if st.button("Previous"):
            self.prev_step()

    def step_3_work_and_weather_preferences(self):
        st.subheader("Step 3: Work and Weather Preferences")
        typical_outfits = self.select_items([
            'Corporate (e.g., suits, formal attire)',
            'Semi-Formal (e.g., dress shirts, slacks, skirts)',
            'Casual (e.g., jeans, casual tops)',
            'Uniform (e.g., scrubs, specific work attire)',
            'Other (Please specify)'
        ], "typical_outfits")

        weather = self.select_items(['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy', 'Stormy'], "weather")

        if typical_outfits and weather:
            if st.button("Next"):
                st.session_state.responses['Work_Attire'] = typical_outfits
                st.session_state.responses['Weather'] = weather
                self.next_step()

        if st.button("Previous"):
            self.prev_step()

    def step_4_fashion_profile(self):
        st.subheader("Step 4: Fashion Profile")
        st.markdown("This is where we get to know your fashion choices as an individual")

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

        styles = self.select_items([
            'Grungy', 'Sexy', 'Casual', 'Laidback/Comfy', 'Classy', 'Showy', 'Colorful',
            'Formal', 'Bohemian', 'Streetwear', 'All of the above'
        ], "styles")

        if date_outfits_frequency and casual_frequency and work_outfits_frequency and styles:
            if st.button("Next"):
                st.session_state.responses['Date_Outfits_Frequency'] = date_outfits_frequency
                st.session_state.responses['Casual_Frequency'] = casual_frequency
                st.session_state.responses['Work_Outfits_Frequency'] = work_outfits_frequency
                st.session_state.responses['Preferred_Styles'] = styles
                self.next_step()

        if st.button("Previous"):
            self.prev_step()

    def step_5_fit_and_style_preferences(self):
        st.subheader("Step 5: Fit and Style Preferences")
        bottoms = self.select_items(['Trousers', 'Shorts', 'Skirts', 'Other'], "bottoms")
        tops = self.select_items(['T-shirts', 'Sweaters', 'Sweatshirts', 'Tanks', 'Other'], "tops")
        shoes = self.select_items(['Sneakers', 'Boots', 'Sandals', 'Flats', 'Heels', 'Other'], "shoes")
        colors = self.select_items([
            'Neutrals and Basics (Beiges, Black, Grays, White, Navy, Browns)',
            'Brights and Bold Colors (Reds, Oranges, Yellows, Greens, Blues)',
            'Soft and Pastel Colors (Pinks, Purples, Teal)',
            'Metallics and Special Colors (Gold, Silver, Burgundy)',
            'Other (Please specify)'
        ], "colors")

        fit_preferences = self.select_items(['Loose', 'Fitted', 'Top Fitted, Bottom Loose', 'Bottom Fitted, Top Loose'], "fit_preferences")

        silhouette = st.radio("Silhouette:", [
            'Hourglass', 'Apple/Round', 'Pear', 'Rectangle/Straight', 'Inverted Triangle', 'Oval/Circle', 'Athletic/Rectangle'
        ])

        if bottoms and tops and shoes and colors and fit_preferences and silhouette:
            if st.session_state.get('logged_in', False):
                st.session_state.responses.update({
                    'Bottom_Type': bottoms,
                    'Top_Type': tops,
                    'Shoe_Type': shoes,
                    'Colors': colors,
                    'Fit_Preferences': fit_preferences,
                    'Silhouette': silhouette,
                    'ID': self.user_id,
                })

                if self.existing_response:
                    update_survey_response(self.user_id, st.session_state.responses)  # Update the existing response
                    st.success("Survey responses updated successfully!")
                else:
                    insert_survey_response(st.session_state.responses)  # Submit a new survey response
                    st.success("Survey submitted successfully!")

                st.rerun()

            else:
                # Call the registration page if not logged in
                registration_page(email=st.session_state.responses.get('Email'))
                # After successful registration, the user will be logged in and the survey can be resubmitted

    def display(self):
        if self.existing_response:
            self.check_existing_response()  # Check and handle existing response logic

        self.progress_bar()
        if st.session_state.step == 0:
            self.step_1_basic_information()
        elif st.session_state.step == 1:
            self.step_2_valentines_day_questions()
        elif st.session_state.step == 2:
            self.step_3_work_and_weather_preferences()
        elif st.session_state.step == 3:
            self.step_4_fashion_profile()
        elif st.session_state.step == 4:
            self.submit_form()


class Recommender:
    def __init__(self, responses):
        self.responses = responses
        self.outfits_df = pd.read_csv('data/final_outfit_characteristics.csv')
        self.outfits_df = self.outfits_df.astype(str)

    def recommend(self):
        threshold = 11
        matched_outfits = defaultdict(list)
        outfit_attributes = set(self.outfits_df.columns.values)
        outfit_attributes.remove("ID")

        def has_match(user_value, outfit_value):
            if type(user_value) != str or type(outfit_value) != str:
                return False
            user_value = set([v.strip() for v in user_value.split(";")])
            outfit_value = set([v.strip() for v in outfit_value.split(";")])
            return len(user_value.intersection(outfit_value)) > 0
 
        user_gender = self.responses.get('Gender', '')

        for _, outfit_data in self.outfits_df.iterrows():
            if outfit_data['Gender'] != user_gender:
                continue

            matched_attribute_count = 0
            for attribute in outfit_attributes:
                if has_match(outfit_data[attribute], self.responses.get(attribute, '')):
                    matched_attribute_count += 1

            if matched_attribute_count >= threshold:
                matched_outfits[outfit_data["ID"]].append(outfit_data["ID"])

        matched_outfit_count = len(matched_outfits)
        table_data = [[self.responses.get('Name', 'User'), f"{matched_outfit_count} matched outfits"]]
        st.write(table_data)

def main():
    user = st.session_state.get('user', None)
    st.header('Les Fashion Secrets')
    st.divider()
    st.markdown("""
    Hi everyone!
                
    Thank you for being a part of Les Fashion Secrets. Together, let’s make this Valentine’s Day and every day unforgettable! ❤️
    """)
    st.write("About you!\nYour information is highly confidential, the following information is for internal research purposes only, all information will not be shared externally.")
    st.divider()
    
    if user:
        survey = Survey(user)
        survey.display()
    else:
        survey = Survey(None)
        survey.display()

if __name__ == '__main__':
    main()
