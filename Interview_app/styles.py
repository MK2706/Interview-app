#!/usr/bin/env python
# coding: utf-8

# In[ ]:


custom_css = """
    <style>
        /* Global background color */
        body {
            background-color: #d3d3d3 !important;  /* Light grey background for all pages */
        }

        /* Title styling */
        h1 {
            font-size: 36px !important;
            color: #005f6b !important;
            text-align: center !important;
            margin-bottom: 20px !important;
        }

        /* Header styling */
        h2 {
            font-size: 30px !important;
            color: #003d47 !important;
            margin-bottom: 10px !important;
        }

        /* Button Styling */
        .stButton>button {
            background-color: #000000 !important; /* Black color for buttons */
            color: white !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            padding: 8px 15px !important;
            width: 100% !important;
        }
        .stButton>button:hover {
            background-color: #333333 !important; /* Dark grey for hover effect */
        }

        /* Section Title Styling */
        .section-header {
            color: #003d47 !important;
            font-size: 24px !important;
            margin-bottom: 10px !important;
        }

        /* Text Area Styling */
        .stTextArea>div>textarea {
            background-color: #ffffff !important;
            color: #333333 !important;
            border: 1px solid #005f6b !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 16px !important;
        }

        /* Chat Message Container Styling */
        .chat-message {
            background-color: #ffffff !important;
            border: 1px solid #ddd !important;
            border-radius: 8px !important;
            padding: 10px !important;
            margin-bottom: 10px !important;
        }

        /* User Message Styling */
        .user {
            background-color: #e1f5fe !important;
            border-color: #80deea !important;
        }

        /* Bot Message Styling */
        .bot {
            background-color: #c8e6c9 !important;
            border-color: #81c784 !important;
        }

        /* Positioning of buttons */
        .bottom-buttons {
            position: fixed !important;
            bottom: 10px !important;
            left: 10px !important;
            right: 10px !important;
            display: flex !important;
            justify-content: space-evenly !important;
            padding: 10px !important;
        }

        /* Padding for content above the buttons */
        .content {
            padding-bottom: 60px !important;
        }
    </style>
"""

