#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from database import connect_to_mongodb

def admin_portal(db):
    st.markdown('<h2 class="section-header">Admin Portal</h2>', unsafe_allow_html=True)

    # Sidebar to display added questions
    st.sidebar.markdown('<h3 class="section-header">Added Questions</h3>', unsafe_allow_html=True)
    
    # Fetch all questions from the database
    all_questions = list(db.questions.find())
    
    # Group questions by job role
    questions_by_role = {}
    for question in all_questions:
        role = question["job_role"]
        if role not in questions_by_role:
            questions_by_role[role] = []
        questions_by_role[role].append(question["question"])
    
    # Display questions by job role in the sidebar
    for role, questions in questions_by_role.items():
        st.sidebar.markdown(f'<h4>{role}</h4>', unsafe_allow_html=True)
        for i, question in enumerate(questions, 1):
            st.sidebar.markdown(f'{i}. {question}')

    # Manage Job Roles
    st.markdown('<h3 class="section-header">Manage Job Roles</h3>', unsafe_allow_html=True)
    new_job_role = st.text_input("Add a new job role")
    if st.button("Add Job Role"):
        if new_job_role and new_job_role not in st.session_state.job_roles:
            st.session_state.job_roles.append(new_job_role)
            st.success(f"Job role '{new_job_role}' added successfully!")
        else:
            st.error("Job role already exists or is invalid.")

    # Set Number of Questions
    st.markdown('<h3 class="section-header">Set Number of Questions</h3>', unsafe_allow_html=True)
    st.session_state.num_questions = st.number_input("Number of Questions for Interview", min_value=1, max_value=50, value=st.session_state.num_questions)

    # Manage Questions
    st.markdown('<h3 class="section-header">Manage Questions</h3>', unsafe_allow_html=True)
    admin_option = st.selectbox("Choose an action", ["Add Question", "Modify Question", "Remove Question"])
    
    if admin_option == "Add Question":
        new_question = st.text_input("Enter a new question")
        new_role = st.selectbox("Select Job Role for New Question", st.session_state.job_roles)
        if st.button("Add Question"):
            db.questions.insert_one({"job_role": new_role, "question": new_question})
            st.success("Question added successfully!")
            st.rerun()  # Refresh to update the sidebar
    
    elif admin_option == "Modify Question":
        question_list = [q for q in db.questions.find()]
        if question_list:
            selected_question = st.selectbox("Select a question to modify", [q["question"] for q in question_list])
            modified_question = st.text_input("Modify the question", selected_question)
            if st.button("Update Question"):
                db.questions.update_one({"question": selected_question}, {"$set": {"question": modified_question}})
                st.success("Question updated successfully!")
                st.rerun()  # Refresh to update the sidebar
        else:
            st.warning("No questions available to modify.")
    
    elif admin_option == "Remove Question":
        question_list = [q for q in db.questions.find()]
        if question_list:
            selected_question = st.selectbox("Select a question to remove", [q["question"] for q in question_list])
            if st.button("Remove Question"):
                db.questions.delete_one({"question": selected_question})
                st.success("Question removed successfully!")
                st.rerun()  # Refresh to update the sidebar
        else:
            st.warning("No questions available to remove.")

    # View Candidate Records
    st.markdown('<h3 class="section-header">Candidate Records</h3>', unsafe_allow_html=True)
    candidate_records = db.candidate_responses.find()
    if candidate_records:
        records_list = []
        for record in candidate_records:
            records_list.append({
                "Username": record["username"],
                "Job Role": record["job_role"],
                "Questions": "\n".join(record["questions"]),
                "Responses": "\n".join(record["responses"]),
                "Feedback": "\n".join(record["feedback"]),
                "Average Score": record.get("average_score", "N/A")  # Display average score
            })
        df = pd.DataFrame(records_list)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download as CSV", csv, "candidate_records.csv", "text/csv")
    else:
        st.warning("No candidate records found.")

