from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import bcrypt
import uuid
import datetime
import urllib

def get_db():
    # uri = st.secrets["MONGO_URI_HOST"] + st.secrets["MONGO_USER"] + urllib.parse.quote(st.secrets["MONGO_PASSWORD"]) + st.secrets["MONGO_URI_SERVER"]
    uri_streamlit = st.secrets["MONGO_URI_HOST"]+ st.secrets["MONGO_USER"] + urllib.parse.quote(st.secrets["MONGO_PASSWORD"]) + st.secrets["MONGO_URI_SERVER2"]
    client = MongoClient(uri_streamlit, server_api=ServerApi('1'))
    db = client[st.secrets["MONGO_DB_NAME"]]
    return db

def insert_user(email, name, username, password):
    db = get_db()
    user_collection = db['users']
    hashed_password = hash_password(password)  # Hash the password before storing it
    user_data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "username": username,
        "password_hash": hashed_password,  # Store the hashed password
        "created at": datetime.datetime.now(datetime.timezone.utc),
        "updated at": datetime.datetime.now(datetime.timezone.utc)
    }
    user_collection.insert_one(user_data)

def find_user_by_email(email):
    db = get_db()
    users = db['users']
    user = users.find_one({"email": email})
    return user

def insert_survey_response(response):
    db = get_db()
    survey_collection = db['survey_collections']
    survey_data = {
        "id": response['ID'],
        "email": response['Email'],
        "name": response['Name'],
        "responses": response,
        "submitted_at": datetime.datetime.now(datetime.timezone.utc)
    }
    survey_collection.insert_one(survey_data)

def get_responses_by_email(email):
    db = get_db()
    responses = db['responses']
    user_responses = responses.find({"email": email})
    return list(user_responses)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
