
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib
import streamlit as st

uri = st.secrets["MONGO_URI_HOST"] + st.secrets["MONGO_USER"] + urllib.parse.quote(st.secrets["MONGO_PASSWORD"]) + st.secrets["MONGO_URI_SERVER"]

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)