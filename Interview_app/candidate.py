#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from database import connect_to_mongodb
from gemini import generate_question, evaluate_response
from utils import extract_score, calculate_average_score

def candidate_portal(db, model):
    st.markdown('<h2 class="section-header">Candidate Portal</h2>', unsafe_allow_html=True)

    # Job role selection
    st.session_state.selected_role = st.selectbox("Select Job Role", st.session_state.job_roles)

    # Start Interview
    if st.button("Start Interview"):
        st.session_state.interview_started = True
        st.session_state.current_question_index = 0  # Reset question index
        st.session_state.user_responses = []  # Reset user responses
        st.session_state.feedback = []  # Reset feedback
        st.session_state.questions = []  # Reset questions
        st.rerun()  # Refresh the page to show the interview interface

    # Interview Interface
    if st.session_state.interview_started:
        st.markdown(f'<h2 class="section-header">{st.session_state.selected_role} Interview</h2>', unsafe_allow_html=True)

        # Fetch questions from the database for the selected role
        if not st.session_state.questions:  # Fetch questions only once
            st.session_state.questions = [q["question"] for q in db.questions.find({"job_role": st.session_state.selected_role})]
            
            # If fewer questions are added than the total number specified, generate the remaining questions using the API
            if len(st.session_state.questions) < st.session_state.num_questions:
                remaining_questions = st.session_state.num_questions - len(st.session_state.questions)
                for _ in range(remaining_questions):
                    generated_question = generate_question(model, st.session_state.selected_role)
                    if generated_question:
                        st.session_state.questions.append(generated_question)

        # Display current question
        if st.session_state.current_question_index < len(st.session_state.questions):
            current_question = st.session_state.questions[st.session_state.current_question_index]
            st.markdown(f'<div class="chat-message"><h3>Question {st.session_state.current_question_index + 1}:</h3><p>{current_question}</p></div>', unsafe_allow_html=True)

            # User response
            response_key = f"response_{st.session_state.current_question_index}"  # Unique key for each question
            response = st.text_input("Your Answer", key=response_key)

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.current_question_index > 0 and st.button("Previous"):
                    st.session_state.current_question_index -= 1
                    st.rerun()
            with col2:
                if st.session_state.current_question_index < len(st.session_state.questions) - 1 and st.button("Next"):
                    if response:
                        feedback = evaluate_response(model, current_question, response)
                        if feedback:
                            st.session_state.user_responses.append(response)
                            st.session_state.feedback.append(feedback)
                            st.session_state.current_question_index += 1
                            # Clear the previous response only if it exists
                            if st.session_state.current_question_index > 0:
                                st.session_state[f"response_{st.session_state.current_question_index - 1}"] = ""
                            st.rerun()
                    else:
                        st.error("Please provide an answer before proceeding.")
            with col3:
                if st.session_state.current_question_index == len(st.session_state.questions) - 1 and st.button("Submit"):
                    if response:
                        feedback = evaluate_response(model, current_question, response)
                        if feedback:
                            st.session_state.user_responses.append(response)
                            st.session_state.feedback.append(feedback)
                            st.success("Interview completed! Thank you for your responses.")
                            
                            # Calculate average score
                            average_score = calculate_average_score(st.session_state.feedback)
                            
                            # Save candidate responses to MongoDB
                            db.candidate_responses.insert_one({
                                "username": st.session_state.username,
                                "job_role": st.session_state.selected_role,
                                "questions": st.session_state.questions,
                                "responses": st.session_state.user_responses,
                                "feedback": st.session_state.feedback,
                                "scores": [extract_score(fb) for fb in st.session_state.feedback],  # Store individual scores
                                "average_score": average_score  # Store average score
                            })
                            
                            st.session_state.logged_in = False  # Logout after submission
                            st.session_state.interview_started = False
                            st.rerun()
                    else:
                        st.error("Please provide an answer before submitting.")

            # Display feedback if available
            if st.session_state.current_question_index < len(st.session_state.feedback):
                st.markdown(f'<div class="chat-message bot"><h3>Feedback:</h3><p>{st.session_state.feedback[st.session_state.current_question_index]}</p></div>', unsafe_allow_html=True)

