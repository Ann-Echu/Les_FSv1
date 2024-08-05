from pymongo import MongoClient
import streamlit as st

def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    db = client[st.secrets["MONGO_DB_NAME"]]
    return db

def insert_user(email, username, password):
    db = get_db()
    users = db.users
    user_data = {
        "email": email,
        "username": username,
        "password": password
    }
    users.insert_one(user_data)

def find_user_by_email(email):
    db = get_db()
    users = db.users
    user = users.find_one({"email": email})
    return user

def insert_response(email, response):
    db = get_db()
    responses = db.responses
    response_data = {
        "email": email,
        "response": response
    }
    responses.insert_one(response_data)

def get_responses_by_email(email):
    db = get_db()
    responses = db.responses
    user_responses = responses.find({"email": email})
    return list(user_responses)
