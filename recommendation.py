import streamlit as st
import pandas as pd
from collections import defaultdict
from utils import get_user_survey_response, update_survey_response, insert_survey_response, registration_page
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change this to control what levels are shown
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler(os.path.join(log_dir, "app.log")), # for file logging
        logging.StreamHandler()  # Log to the console only
    ]
)

class Survey:
    """
    Survey provides users with the survey questions for the algorithm
    """
    def __init__(self, user):
        self.user = user
        self.user_id = st.session_state.get('user_id') if user else None # setting to None since user is not authenticated
        self.responses = {}
        self.step = 0
        self.total_steps = 6
        self.initialize_session_state()
        self.existing_response = get_user_survey_response(self.user_id) if user else None  # Check if the user has an existing survey response

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
        st.markdown("How would you describe your current relationship status?")
        relationship_status = st.radio(
            "Choose relation status: ",
            ['Single', 'In a relationship', 'Married', 'Separated/Divorced', 'Widowed', 'Prefer not to say', 'Other']
        )
        if relationship_status == 'Other':
            other_status = st.text_input("Please specify your relationship status:")
            relationship_status = other_status if other_status else relationship_status

        st.markdown("Please select your gender:")
        gender = st.radio(
            "Gender Choices: ",
            ['Woman', 'Man', 'Non-binary', 'Prefer not to say', 'Other']
        )
        if gender == 'Other':
            other_gender = st.text_input("Please specify:")
            gender = other_gender if other_gender else gender

        st.markdown("How old are you?")
        age = st.radio(
            "Age Category:",
            ['Under 18: Youth', '18-24: Young Adult', '25-34: Adult', '35-44: Mid-Adult', '45-54: Senior-Adult', '55 or over: Senior']
        )

        if relationship_status and gender and age:
            if st.button("Next"):
                st.session_state.responses['Relationship_Status'] = relationship_status
                st.session_state.responses['Gender'] = gender
                st.session_state.responses['Age'] = age
                self.next_step()

    def step_2_valentines_day_questions(self):
        st.subheader("Step 2: Valentine's Day Questions")
        
        st.markdown("How are you planning to spend Valentine's Day this year?")
        valentines_plans = st.radio(
            "Valentines day plans",
            ['Celebrating with a partner', 'Enjoying a day with friends or family', 'Treating myself to something special', 
            'Not planning anything specific', 'Prefer not to say', 'Other']
        )
        if valentines_plans == 'Other':
            other_plans = st.text_input("Please specify your plans:")
            valentines_plans = other_plans if other_plans else valentines_plans

        st.markdown("What are your plans for Valentines Day?")
        valentines_activities = self.select_items(
            ['Dinner date', 'Casual outing (e.g. Picnic, movies)', 'Romantic getaway', 'Staying in', 'Other'], 
            "valentines_activities"
        )
        if 'Other' in valentines_activities:
            other_valentines_activties = st.text_input("Please specify:")
            if other_valentines_activties:
                valentines_activities.append(other_valentines_activties) 

        st.markdown("Do you have a preference for certain types of outfits for Valentine’s Day? ")
        valentines_outfits = self.select_items(
            ['Elegant/Formal (e.g., dresses, suits)', 'Casual/Comfortable (e.g., jeans, sweaters)', 'Trendy/Fashion-forward (e.g., stylish outfits, current trends)',
             'Romantic/Sexy (e.g., cocktail dresses, tailored outfits)', 'Laidback/Comfy (e.g., loungewear, casual chic)'], 
             "valentines_outfits"
        )

        if 'Other' in valentines_outfits:
            other_valentines_outfits = st.text_input("Please specify:")
            if other_valentines_outfits:
                valentines_outfits.append(other_valentines_outfits) 


        st.markdown("Which colors would you prefer to wear for Valentine's Day")
        valentines_colors = self.select_items(
            ['Red', 'Pink', 'White', 'Black', 'No color preference', 'Other colors'], 
            "valentines_colors"
        )

        if 'Other colors' in valentines_colors:
            other_valentines_colors = st.text_input("Please specify:")
            if other_valentines_colors:
                valentines_colors.append(other_valentines_colors) 

        if valentines_plans and valentines_activities and valentines_outfits and valentines_colors:
            if st.button("Next"):
                st.session_state.responses['Valentines_Plans'] = valentines_plans
                st.session_state.responses['Valentines_Activities'] = valentines_activities
                st.session_state.responses['Valentines_Outfits'] = valentines_outfits
                st.session_state.responses['Valentines_Colors'] = valentines_colors
                self.next_step()

        if st.button("Previous"):
            self.prev_step()

    def step_3_work_and_weather_preferences(self):
        st.subheader("Step 3: Work and Weather Preferences")
        st.markdown("What type of outfits do you typically wear for work?")
        typical_outfits = self.select_items([
            'Corporate (e.g., suits, formal attire)',
            'Semi-Formal (e.g., dress shirts, slacks, skirts)',
            'Casual (e.g., jeans, casual tops)',
            'Uniform (e.g., scrubs, specific work attire)',
            'Other'
        ], "typical_outfits")

        if 'Other' in typical_outfits:
            other_typical_outfits = st.text_input("Please specify:")
            if other_typical_outfits:
                typical_outfits.append(other_typical_outfits) 

        st.markdown("What’s the weather like during Valentine’s Day?")
        valentines_weather = st.radio(
                    "Weather in your city:",
                    ['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy', 'Stormy', 'Other']
                    )
        if valentines_weather == 'Other':
            other_weather = st.text_input("Please specify the weather:")
            valentines_weather = other_weather if other_weather else valentines_weather

        if typical_outfits and valentines_weather:
            if st.button("Next"):
                st.session_state.responses['Work_Attire'] = typical_outfits
                st.session_state.responses['Weather'] = valentines_weather
                self.next_step()

        if st.button("Previous"):
            self.prev_step()

    def step_4_fashion_profile(self):
        st.subheader("Step 4: Fashion Profile")
        st.markdown("This is where we get to know your fashion choices as an individual")

        st.markdown("In a month")
        date_outfits_frequency = st.radio(
            "How often would you wear date nights/night outs outfits? ",
            ['Rarely', 'Sometimes', 'Often', 'Never'],
            horizontal=True
        )

        casual_frequency = st.radio(
            "How often would you wear casual outfits?",
            ['Rarely', 'Sometimes', 'Often', 'Never'],
            horizontal=True
        )

        work_outfits_frequency = st.radio(
            "How often would you wear outfits for work?",
            ['Rarely', 'Sometimes', 'Often', 'Never'],
            horizontal=True
        )

        st.markdown("What are your preferred styles?")
        styles = self.select_items([
            'Grungy', 'Sexy', 'Casual', 'Laidback/Comfy', 'Classy', 'Showy', 'Colorful',
            'Formal', 'Bohemian', 'Streetwear', 'All of the above', 'Other'
        ], "styles")

        if 'Other' in styles:
            other_styles = st.text_input("Please specify:")
            if other_styles:
                styles.append(other_styles) 

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

        st.markdown("Which type of bottoms do you prefer?")
        bottoms = self.select_items(['Trousers', 'Shorts', 'Skirts', 'Other'], "bottoms")
        if 'Other' in bottoms:
            other_bottoms = st.text_input("Please specify:")
            if other_bottoms:
                bottoms.append(other_bottoms) 

        st.markdown("Which type of tops do you prefer?")
        tops = self.select_items(['T-shirts', 'Sweaters', 'Sweatshirts', 'Tanks', 'Other'], "tops")
        if 'Other' in tops:
            other_tops = st.text_input("Please specify:")
            if other_tops:
                tops.append(other_tops) 

        st.markdown("Which type of shoes do you prefer?")
        shoes = self.select_items(['Sneakers', 'Boots', 'Sandals', 'Flats', 'Heels', 'Other'], "shoes")
        
        if 'Other' in shoes:
            other_shoes = st.text_input("Please specify:")
            if other_shoes:
                shoes.append(other_shoes) 

        st.markdown("What colors do you prefer for your clothes?")
        colors = self.select_items([
            'Neutrals and Basics (Beiges, Black, Grays, White, Navy, Browns)',
            'Brights and Bold Colors (Reds, Oranges, Yellows, Greens, Blues)',
            'Soft and Pastel Colors (Pinks, Purples, Teal)',
            'Metallics and Special Colors (Gold, Silver, Burgundy)',
            'Other'
        ], "colors")

        if 'Other' in colors:
            other_colors = st.text_input("Please specify:")
            if other_colors:
                colors.append(other_colors) 

        st.markdown("Do you like your clothes loose or fitted? ")
        fit_preferences = self.select_items(['Loose', 'Fitted', 'Top Fitted, Bottom Loose', 'Bottom Fitted, Top Loose'], "fit_preferences")
        if 'Other' in fit_preferences:
            other_fit_preferences = st.text_input("Please specify:")
            if other_fit_preferences:
                fit_preferences.append(other_fit_preferences) 
        
        st.markdown("Please select the option that best describes your silhouette")
        silhouette = st.radio("Please select your silhouette:", [
            'Hourglass: Curvy waist, balanced hips, bust', 
            'Apple/Round: Round midsection, less defined waist',
            'Pear: Wider hips, narrower shoulders', 
            'Rectangle/Straight: Even proportions, straight silhouette', 
            'Inverted Triangle: Broad shoulders, narrower hips', 
            'Oval/Circle: Round midsection, fuller bust',
            'Athletic/Rectangle: Muscular, even proportions, athletic build'
        ])

        if 'Other' in silhouette:
            other_silhouette = st.text_input("Please specify:")
            if other_silhouette:
                silhouette.append(other_silhouette) 


        if bottoms and tops and shoes and colors and fit_preferences and silhouette:
            if st.session_state.get('logged_in', False):
                st.session_state.responses.update({
                    'Bottom_Type': bottoms,
                    'Top_Type': tops,
                    'Shoe_Type': shoes,
                    'Colors': colors,
                    'Fit_Preferences': fit_preferences,
                    'Silhouette': silhouette,
                    'Name': self.user['name'],
                    'ID': self.user_id,
                    'Email': self.user['email']
                })
                
                logging.info(st.session_state.responses)
                if self.existing_response:
                    update_survey_response(self.user_id, st.session_state.responses)  # Update the existing response
                    st.success("Survey responses updated successfully!")
                else:
                    insert_survey_response(st.session_state.responses)  # Submit a new survey response
                    st.success("Survey submitted successfully!")
                    # st.switch_page("")
                

                st.rerun()

            else:
                # Call the registration page if not logged in
                registration_page()
                # After successful registration, the user will be logged in and the survey can be resubmitted

    def display(self):
        # check if response exist, else set as none
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
            self.step_5_fit_and_style_preferences()



class Recommender:
    """
    The class handles the recommendation of outfits
    """
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
    """
    Returns: None
    The main function for the recommendation.py class

    """
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
