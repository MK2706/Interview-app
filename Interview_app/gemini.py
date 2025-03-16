#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import google.generativeai as genai
import os

# Initialize Gemini API
def initialize_gemini():
    gemini_api_key = os.getenv("GEMINI_API_KEY", "GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Generate interview question
def generate_question(model, job_role):
    try:
        prompt = f"Generate an interview question for the role of {job_role}."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Failed to generate question: {e}")
        return None

# Evaluate candidate response
def evaluate_response(model, question, response):
    try:
        prompt = f"Question: {question}\nResponse: {response}\n\nEvaluate the response first give the score out of 10 and give feedback in new line  and don't give the answer for the question."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Failed to evaluate response: {e}")
        return None

