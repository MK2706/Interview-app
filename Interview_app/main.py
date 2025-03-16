#!/usr/bin/env python
# coding: utf-8

# In[ ]:
pip install -r requirements.txt

import streamlit as st
from database import connect_to_mongodb, hash_password, verify_password
from gemini import initialize_gemini
from admin import admin_portal
from candidate import candidate_portal
from styles import custom_css

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Gemini model
model = initialize_gemini()

# Connect to MongoDB
db = connect_to_mongodb()

def main():
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Initialize Gemini model
    model = initialize_gemini()

    # Connect to MongoDB
    db = connect_to_mongodb()

    if db is None:
        st.error("Failed to connect to MongoDB. Please check your connection settings.")
        return

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "show_login" not in st.session_state:
        st.session_state.show_login = True
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = None
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = []
    if "feedback" not in st.session_state:
        st.session_state.feedback = []
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "job_roles" not in st.session_state:
        # Initialize job_roles as an empty list
        st.session_state.job_roles = []
    if "num_questions" not in st.session_state:
        st.session_state.num_questions = 5  # Default number of questions

    # Fetch job roles from the database
    job_roles_collection = db.job_roles  # Use the job_roles collection
    st.session_state.job_roles = [role["name"] for role in job_roles_collection.find()]

    # Login and Signup Section
    if not st.session_state.logged_in:
        st.markdown('<h2 class="header">Login or Signup</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_button_1"):
                st.session_state.show_login = True
        with col2:
            if st.button("Signup", key="login_button_2"):
                st.session_state.show_login = False

        # Show login or signup form based on button click
        if st.session_state.show_login:
            # Login Form
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = db.users.find_one({"username": username})
                if user:
                    if verify_password(password, user["password"]):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.is_admin = user.get("role") == "admin"
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("User not found.")
        else:
            # Signup Form
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            if st.button("Signup"):
                if new_password == confirm_password:
                    if db.users.find_one({"username": new_username}):
                        st.error("Username already exists. Please choose a different username.")
                    else:
                        hashed_password = hash_password(new_password)
                        db.users.insert_one({
                            "username": new_username,
                            "password": hashed_password.decode('utf-8'),
                            "role": "candidate"
                        })
                        st.success("Account created successfully! Please log in.")
                else:
                    st.error("Passwords do not match.")

    # Main App Interface (Only show if logged in)
    if st.session_state.logged_in:
        # Add a logout button in the top-right corner
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.is_admin = False
                st.session_state.show_login = True
                st.session_state.interview_started = False
                st.session_state.current_question_index = 0
                st.session_state.user_responses = []
                st.session_state.feedback = []
                st.success("Logged out successfully!")
                st.rerun()

        # Admin Portal
        if st.session_state.is_admin:
            admin_portal(db)
        # Candidate Portal
        else:
            if not st.session_state.job_roles:
                st.warning("No job roles available. Please contact the admin to add job roles.")
            else:
                candidate_portal(db, model)

# Run the app
if __name__ == "__main__":
    main()

