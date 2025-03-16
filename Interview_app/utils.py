#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re

# Extract score from feedback
def extract_score(feedback):
    match = re.search(r"Score:\s*(\d+)/10", feedback)
    if match:
        return int(match.group(1))
    return None

# Calculate average score
def calculate_average_score(feedback_list):
    scores = []
    for feedback in feedback_list:
        score = extract_score(feedback)
        if score is not None:
            scores.append(score)
    if scores:
        return sum(scores) / len(scores)
    return None

