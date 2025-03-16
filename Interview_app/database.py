#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from urllib.parse import quote_plus
import os
import bcrypt

# MongoDB connection
def connect_to_mongodb():
    try:
        username = os.getenv("MONGODB_USERNAME", "manojmn2703")
        password = os.getenv("MONGODB_PASSWORD", "1Kumar@26")  # Use environment variables for security
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.oou3r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        client = MongoClient(connection_string, serverSelectionTimeoutMS=60000)
        client.server_info()  # Test connection
        print("Connected to MongoDB!")
        return client["interview_app"]  # Replace with your database name
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return None
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
def verify_password(plain_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

