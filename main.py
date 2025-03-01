import streamlit as st
import os
import random
import pandas as pd
import numpy as np
from PIL import Image

# Define CSV files and image folders for different languages
CSV_FILES = {
    "Yoruba": "data/YOR/2010/2010.csv",  
    "Igbo": "data/igbo_questions/IGBO.csv"
}
IMAGE_FOLDERS = {
    "Yoruba": "2010/",  
    "Igbo": "data/igbo_questions"
}
RESPONSES_FILE = "responses.csv"  # File to store user responses

# Load previous responses if they exist
if os.path.exists(RESPONSES_FILE):
    responses_df = pd.read_csv(RESPONSES_FILE)
else:
    responses_df = pd.DataFrame(columns=["username", "language", "image_id", "user_answer"])

# Initialize session state for user details, language selection, and progress
if "username" not in st.session_state:
    st.session_state.username = None
if "language" not in st.session_state:
    st.session_state.language = None
if "remaining_indices" not in st.session_state:
    st.session_state.remaining_indices = None
    st.session_state.current_index = None
    st.session_state.user_answers = []
# Initialize session state for tracking progress
if "total_questions" not in st.session_state:
    st.session_state.total_questions = None
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = 0

# First page to collect username and language choice
if st.session_state.username is None or st.session_state.language is None:
    st.title("Welcome to the Quiz!")
    username = st.text_input("Enter your name to start:")
    language = st.selectbox("Select a language:", ["Yoruba", "Igbo"], index=None, placeholder="Choose...")

    if st.button("Start Quiz") and username and language:
        st.session_state.username = username
        st.session_state.language = language
        data = pd.read_csv(CSV_FILES[language])
        st.session_state.data = data  # Store the dataset
        st.session_state.image_folder = IMAGE_FOLDERS[language]  # Store image folder
        st.session_state.remaining_indices = list(range(len(data)))
        random.shuffle(st.session_state.remaining_indices)
        st.session_state.total_questions = len(data)  # Track total questions
        st.session_state.current_index = st.session_state.remaining_indices.pop()
        st.rerun()
    st.stop()

# Display progress counter
st.sidebar.write(f"📊 **Progress:** {st.session_state.answered_questions} / {st.session_state.total_questions}")
st.sidebar.write(f"📌 **Questions Left:** {st.session_state.total_questions - st.session_state.answered_questions}")

# Ensure data is loaded from session state
if "data" not in st.session_state:
    st.session_state.data = None  # Initialize data

# Check if all questions are answered
if not st.session_state.remaining_indices and "current_index" not in st.session_state:
    st.write(f"🎉 Thank you for participating, {st.session_state.username}! Goodbye! 👋")
    answers_df = pd.DataFrame(st.session_state.user_answers)
    st.write("Your responses:")
    st.dataframe(answers_df)
    st.stop()

# Load dataset from session state
data = st.session_state.data
if data is None:
    st.error("Data not loaded properly. Please restart the app.")
    st.stop()

# Get current question details
current_row = data.iloc[st.session_state.current_index]
image_path = os.path.join(st.session_state.image_folder, current_row["data_path"])

# Display question image
st.title(f"{st.session_state.language} Quiz for {st.session_state.username}")
st.image(Image.open(image_path), use_container_width=True)

# Answer choices
options = ["A", "B", "C", "D"]
user_choice = st.radio("Select an answer:", options, key=st.session_state.current_index)

# Buttons to submit or skip
col1, col2 = st.columns(2)
with col1:
    if st.button("Next Question"):
        st.session_state.user_answers.append({
            "username": st.session_state.username,
            "language": st.session_state.language,
            "image_id": current_row["data_path"],
            "user_answer": user_choice
        })
        st.session_state.answered_questions += 1  # Increment answered count

        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            del st.session_state.current_index  # End quiz
            st.write(f"🎉 Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            answers_df = pd.DataFrame(st.session_state.user_answers)
            st.write("Your responses:")
            st.dataframe(answers_df)
            st.stop()

with col2:
    if st.button("Skip Question"):
        st.session_state.user_answers.append({
            "username": st.session_state.username,
            "language": st.session_state.language,
            "image_id": current_row["data_path"],
            "user_answer": np.nan
        })
        st.session_state.answered_questions += 1  # Increment answered count

        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            del st.session_state.current_index  # End quiz
            st.write(f"🎉 Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            answers_df = pd.DataFrame(st.session_state.user_answers)
            st.write("Your responses:")
            st.dataframe(answers_df)
            st.stop()