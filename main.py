import streamlit as st
import os
import random
import pandas as pd
from PIL import Image

# Load CSV file with image paths and answers
CSV_FILE = "2010/2010.csv"  # Change to your actual file path
IMAGE_FOLDER = "2010/"  # Change to your folder path

data = pd.read_csv(CSV_FILE)
    
# Initialize session state for user details, questions, and answers
if "username" not in st.session_state:
    st.session_state.username = None
if "remaining_indices" not in st.session_state:
    st.session_state.remaining_indices = list(range(len(data)))
    random.shuffle(st.session_state.remaining_indices)
    st.session_state.current_index = None
    st.session_state.user_answers = []

# First page to collect username
if st.session_state.username is None:
    st.title("Welcome to the Quiz!")
    username = st.text_input("Enter your name to start:")
    if st.button("Start Quiz") and username:
        st.session_state.username = username
        st.session_state.current_index = st.session_state.remaining_indices.pop()
        st.rerun()
    st.stop()

# Check if all questions have been answered
if not st.session_state.remaining_indices and "current_index" not in st.session_state:
    st.write(f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
    # Convert user answers to a DataFrame and display it
    answers_df = pd.DataFrame(st.session_state.user_answers)
    st.write("Your responses:")
    st.dataframe(answers_df)
    st.stop()

# Get current question details
current_row = data.iloc[st.session_state.current_index]
image_path = os.path.join(IMAGE_FOLDER, current_row["image_id"])

# Display the question image
st.title(f"Quiz for {st.session_state.username}")
st.image(Image.open(image_path), use_container_width=True)

# Answer choices
options = ["A", "B", "C", "D"]
user_choice = st.radio("Select an answer:", options, key=st.session_state.current_index)

# Button to submit answer and load a new question
if st.button("Next Question"):
    # Store user response
    st.session_state.user_answers.append({
        "username": st.session_state.username,
        "image_id": current_row["image_id"],
        "user_answer": user_choice
    })
    
    if st.session_state.remaining_indices:
        st.session_state.current_index = st.session_state.remaining_indices.pop()
        st.rerun()
    else:
        del st.session_state.current_index  # Remove current question to stop rerunning
        st.write(f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
        answers_df = pd.DataFrame(st.session_state.user_answers)
        st.write("Your responses:")
        st.dataframe(answers_df)
        st.stop()
