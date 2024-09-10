import streamlit as st
import pandas as pd
from collections import defaultdict
from pathlib import Path

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