from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import bcrypt
import uuid
import datetime
import urllib

def get_db():
    uri = st.secrets["MONGO_URI_HOST"] + st.secrets["MONGO_USER"] + urllib.parse.quote(st.secrets["MONGO_PASSWORD"]) + st.secrets["MONGO_URI_SERVER"]
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[st.secrets["MONGO_DB_NAME"]]
    return db

def insert_user(email, name, username, password):
    db = get_db()
    user_collection = db['users']
    hashed_password = hash_password(password)  # Hash the password before storing it
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "username": username,
        "password_hash": hashed_password,  # Store the hashed password
        "created_at": datetime.datetime.now(datetime.timezone.utc),
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
    }
    user_collection.insert_one(user_data)
    return user_id  # Return the user ID for further use

def find_user_by_email(email):
    db = get_db()
    user_collection = db['users']
    user = user_collection.find_one({"email": email})
    return user

def insert_survey_response(response):
    db = get_db()
    survey_collection = db['survey_responses']
    survey_data = {
        "user_id": response['ID'],
        "email": response['Email'],
        "name": response['Name'],
        "responses": response,
        "submitted_at": datetime.datetime.now(datetime.timezone.utc)
    }
    survey_collection.insert_one(survey_data)

def get_user_survey(user_id):
    db = get_db()
    survey_collection = db['survey_responses']
    user_survey = survey_collection.find_one({"user_id": user_id})
    return user_survey

def update_user_survey(user_id, responses):
    db = get_db()
    survey_collection = db['survey_responses']
    update_data = {
        "responses": responses,
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
    }
    survey_collection.update_one({"user_id": user_id}, {"$set": update_data})

def insert_user_survey(responses):
    db = get_db()
    survey_collection = db['survey_responses']
    
    # Check if the survey already exists for this user
    existing_survey = survey_collection.find_one({"user_id": responses['ID']})

    if existing_survey:
        # Update the existing survey response
        update_data = {
            "responses": responses,
            "updated_at": datetime.datetime.now(datetime.timezone.utc)
        }
        survey_collection.update_one({"user_id": responses['ID']}, {"$set": update_data})
        st.success("Survey responses updated successfully!")
    else:
        # Insert a new survey response
        survey_data = {
            "user_id": responses['ID'],
            "email": responses['Email'],
            "name": responses['Name'],
            "responses": responses,
            "submitted_at": datetime.datetime.now(datetime.timezone.utc)
        }
        survey_collection.insert_one(survey_data)
        st.success("Survey submitted successfully!")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
