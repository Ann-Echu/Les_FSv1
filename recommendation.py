import streamlit as st
import pandas as pd
from collections import defaultdict
from collections import OrderedDict
import random
# from tabulate import tabulate

#helper function to handle and display multiboxes.
def select_items(item_list, prefix):
    selected_items = []
    for idx, item in enumerate(item_list):
        if st.checkbox(item, key=f"{prefix}_{idx}"):
            selected_items.append(item)
    return selected_items

def __recommender(name):
    # print(responses)
    user_preferences_df = pd.read_csv('responses.csv')
    outfits_df = pd.read_csv('final_outfit_characteristics.csv')

    # # Ensure both dataframes have the same columns before concatenating
    if list(user_preferences_df.columns) != list(outfits_df.columns):
        raise ValueError("The columns of user preferences and outfits dataframes do not match.")

    # Convert all columns to strings to ensure uniform data type
    user_preferences_df = user_preferences_df.astype(str)
    outfits_df = outfits_df.astype(str)

    # Define a threshold for matching characteristics
    threshold = 11  # At least 11 matching characteristics out of 16

    def hasMatch(userValue, outfitValue):
        # Check if both values are strings
        if type(userValue) != str or type(outfitValue) != str:
            return False
        
        # Split values into attributes and create sets
        userValue = getSplitAttributes(userValue)
        outfitValue = getSplitAttributes(outfitValue)

        # Check if there is any intersection between user and outfit attributes
        return len(userValue.intersection(outfitValue)) > 0

    def getSplitAttributes(values):
        # Split the values by delimiter ";" and create a set of attributes
        return set([v.strip() for v in values.split(";")])

    # Match user preferences to outfits
    user_outfit_matches = []

    # Dictionary to store matched outfits for each user
    matchedOutfits = defaultdict(list)

    # Set of attributes in outfits dataframe (excluding ID)
    outfitAttributes = set(outfits_df.columns.values)
    outfitAttributes.remove("ID")

    # Iterate over each user and their preferences
    for userIndex, user in user_preferences_df.iterrows():
        # Get user's gender for filtering outfits
        userGender = user['Gender']
        
        # Iterate over each outfit to find matches for the user
        for outfitIndex, outfitData in outfits_df.iterrows():
            # Check if outfit gender matches user's gender
            if outfitData['Gender'] != userGender:
                continue
            
            # Initialize counter for matched attributes
            matchedAttributeCt = 0
            
            # Iterate over each attribute in the outfit
            for attribute in outfitAttributes:
                # Get attribute values for user and outfit
                outfitAttrData = outfitData[attribute]
                userAttrData = user[attribute]
                
                # Check if there is a match between user and outfit attributes
                if hasMatch(outfitAttrData, userAttrData):
                    matchedAttributeCt += 1
            
            # If number of matched attributes exceeds threshold, add outfit to user's matches
            if matchedAttributeCt >= threshold:
                matchedOutfits[userIndex].append(outfitData["ID"])
        
        # Count and print the number of matched outfits for each user
        matchedOutfitCt = len(matchedOutfits[userIndex])
        # print(f"User {userIndex + 1} matched with {matchedOutfitCt} outfits")

    # Print the matched outfits for each user    
    # for userIndex in sorted(matchedOutfits.keys()):
    #     print(f"User {userIndex + 1} outfit matches: {matchedOutfits[userIndex]}")
        
    # Prepare data for table format
    table_data = []
    for userIndex in sorted(matchedOutfits.keys()):
        table_data.append([f"{name}", f"{len(matchedOutfits[userIndex])} matched outfits"])

    # Print the table
    headers = ["Name", "Number of Matched Outfits"]
    st.write(table_data) #headers=headers, tablefmt="pretty")

def main():
    # Create Web-page Layout
    st.header('Les Fashion Secrets')
    st.divider()
    st.markdown("Hi everyone! Thanks for taking part in our survey.\n\
                You're helping us out big time – our academic lives depend on it, quite literally!\n\
                Anyway, this is a brief survey that should only take about 6 minutes of your time.\n\
                We're collecting data on your fashion preferences and choices to help us build a machine\n\
                for our Business Intelligence Project. Thank you again for your time.")

    st.write("About you!\nYour information is highly confidential, the following information is for internal research purpose only, all information will not be shared externally.")
    st.divider()

    # Question about gender
    st.write("*Please select your gender: ")
    gender = st.radio(
        "Choose one:",
        ('Woman','Man','Non-binary','Prefer not to say','Other')
    )
    # handle the other option selected
    if gender == 'Other':
        other_gender = st.text_input("Please specify:")
        gender = other_gender

    # Age
    st.write("*How old are you?")
    age = st.radio(
        "Choose one:",
        ('18-24: YoungAdult','25-34: Adult','35-44: MidAdult','45-54: SeniorAdult','55 or over: Senior')
    )

    # Type of outfits
    st.write("*What type of outfits do you typically wear for work? ")
    typical_outfits_list = [
        'Corporate (e.g., suits, formal attire)',
        'Semi-Formal (e.g., dress shirts, slacks, skirts)', 
        'Casual (e.g., jeans, casual tops)', 
        'Uniform (e.g., scrubs, specific work attire)'
    ]
    typical_outfits = select_items(typical_outfits_list, "typical_outfits")

    # Weather they like
    st.write("*What is the weather like where you are? ")
    weather_list =['Mild','Cool', 'Hot', 'Warm','Cold']
    weather = select_items(weather_list, "weather")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Fashion profile")
    st.markdown("This is where we get to know your fashion choices as an individual")

    # How often do you wear casual clothes
    st.write("How often do you wear casual clothes?")
    casual = st.radio(
        "Casual:",
        ['Rarely', 'Sometimes', 'Often'],
        horizontal=True
    )

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Styles you are looking to get into
    st.write("What styles are you looking to get into? (Select all that apply)")
    styles_list = [
        'Grungy', 'Sexy', 'Casual', 'Laidback', 'Classy', 'Showy', 'Colorful',
        'Formal', 'Bohemian', 'Streetwear', 'All of the above'
    ]
    styles = select_items(styles_list, "styles")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Clothing items you prefer to have or add to your wardrobe
    st.write("Which of the following clothing items do you prefer to have or add to your wardrobe? (Select all that apply)")
    clothing_items_list = [
        'T-shirts (Graphic tees, plain tees, etc.)',
        'Shirts (Button-down shirts, dress shirts, flannel shirts, denim shirts, etc.)',
        'Blouses', 'Sweaters', 'Hoodies', 'Cardigans', 'Blazers',
        'Jeans (Skinny jeans, bootcut jeans, boyfriend jeans, mom jeans, straight jeans, etc.)',
        'Pants (Dress pants, wide-leg pants, high-waisted pants, cargo pants, etc.)',
        'Skirts', 'Shorts', 'Leggings', 'Jumpsuits (Rompers)', 'Mini dresses',
        'Midi dresses', 'Maxi dresses', 'Bodycon dresses', 'Shift dresses',
        'Wrap dresses', 'Cocktail dresses', 'Coats (Trench coats, puffer coats, wool coats, etc.)',
        'Jackets (Leather jackets, denim jackets, etc.)', 'Blazers', 'Sports bras',
        'Athletic tops (Tank tops, etc.)', 'Athletic shorts', 'Sneakers (Converse, etc.)',
        'Boots (Ankle boots, knee-high boots, combat boots, etc.)', 'Sandals',
        'Flats', 'Heels (Pumps, stilettos, block heels, wedges, etc.)', 'Loafers', 'All of the above'
    ]
    clothing_items = select_items(clothing_items_list, "clothing_items")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Type of bottoms you buy most often
    st.write("Which type of bottoms do you buy most often?")
    bottoms_list = ['Trousers', 'Shorts', 'Skirts']
    bottoms = select_items(bottoms_list, "bottoms")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Type of tops you buy most often
    st.write("Which type of tops do you buy most often?")
    tops_list = ['T-shirts', 'Sweaters', 'Sweatshirts', 'Tanks', 'All of the above']
    tops = select_items(tops_list, "tops")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Type of shoes you buy most often
    st.write("Which type of shoes do you buy most often?")
    shoes_list = ['Sneakers', 'Boots', 'Sandals', 'Flats', 'Heels', 'All of the above']
    shoes = select_items(shoes_list, "shoes")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Colors you prefer to wear
    st.write("What colors do you prefer to wear? (Select all that apply)")
    colors_list = [
        'Neutral (Beiges, Black, Browns, Grays, Silver, White)',
        'Warm (Burgundy, Gold, Orange, Red, Yellow, Pink, Purple)',
        'Cool (Blue, Green, Navy, Teal)'
    ]
    colors = select_items(colors_list, "colors")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Patterns you prefer to wear
    st.write("Are there any patterns you prefer to wear?")
    patterns_list = [
        'Animals', 'Dice', 'Florals', 'Paisleys', 'Plaids', 'Polka dots', 'Stripes', 'Plain', 'All of the above'
    ]
    patterns = select_items(patterns_list, "patterns")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Fabrics you prefer to wear
    st.write("Are there any fabrics you prefer to wear?")
    fabrics_list = [
        'Cotton', 'Denim', 'Silk', 'Faux Fur', 'Leather', 'Wool', 'Faux Leather', 'All of the above'
    ]
    fabrics = select_items(fabrics_list, "fabrics")


    # Add space
    st.markdown("<br>", unsafe_allow_html=True)


    st.subheader("Fit and Style Preferences")
    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # How do you prefer clothes to fit your top half?
    st.write("How do you prefer clothes to fit your top half?")
    fit_top_half_list = ['Tight', 'Fitted', 'Straight', 'Loose', 'Oversize']
    fit_top_half = select_items(fit_top_half_list, "fit_top_half")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # How do you prefer clothes to fit your bottom half?
    st.write("How do you prefer clothes to fit your bottom half?")
    fit_bottom_half_list = ['Tight', 'Fitted', 'Straight', 'Loose', 'Oversize']
    fit_bottom_half = select_items(fit_bottom_half_list, "fit_bottom_half")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Your email address
    st.write("State your email address. *")
    email = st.text_area("Your email: ")

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    # Your name
    st.write("State your name.*")
    name = st.text_area("Your name: ")

    ID = int(random.uniform(90, 1000))

    # Dictionary to store all the responses
    responses = {
        'ID': ID,
        'Gender': gender,
        'Age': age,
        'Work_Attire': typical_outfits,
        'Weather': weather,
        'Casual': casual, 
        'Preferred_Styles': styles,
        'Clothing_items': clothing_items,
        'Bottom_Type': bottoms,
        'Top_Type': tops,
        'Shoe_Type': shoes,
        'Colors': colors,
        'Patterns': patterns,
        'Fabrics': fabrics,
        'Top_Fit': fit_top_half,
        'Bottom_Fit': fit_bottom_half,
    }

    # # Submit button
    # if st.button('Submit'):
    #     # Convert dictionary to recommender
    #     # table_data = recommender(responses)
    #     df = pd.DataFrame([responses])
        

    #     # Append data to CSV file
    #     csv_file = 'responses.csv'
    #     try:
    #         existing_df = pd.read_csv(csv_file)
    #         df = pd.concat([existing_df, df], ignore_index=True)
    #     except FileNotFoundError:
    #         df.to_csv(csv_file, index=False)

    #     df.to_csv(csv_file, index=False)
    #     st.success("Responses saved successfully!")
    #     st.write("Outfits")
    #     recommender(name)


if __name__ == '__main__':
    main()