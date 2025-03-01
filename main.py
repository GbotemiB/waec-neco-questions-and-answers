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

# First page to collect username and language choice
if st.session_state.username is None or st.session_state.language is None:
    st.title("Welcome to the Quiz!")
    username = st.text_input("Enter your name to start or resume:")
    language = st.selectbox("Select a language:", ["Yoruba", "Igbo"], index=None, placeholder="Choose...")

    if st.button("Start Quiz") and username and language:
        st.session_state.username = username
        st.session_state.language = language
        data = pd.read_csv(CSV_FILES[language])
        st.session_state.data = data  
        st.session_state.image_folder = IMAGE_FOLDERS[language]

        # Filter out already answered questions
        answered_questions = responses_df[(responses_df["username"] == username) & (responses_df["language"] == language)]["image_id"].tolist()
        st.session_state.remaining_indices = [i for i in range(len(data)) if data.iloc[i]["image_id"] not in answered_questions]

        random.shuffle(st.session_state.remaining_indices)

        # Resume or start fresh
        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
        else:
            st.session_state.current_index = None

        st.rerun()
    st.stop()

# Load selected dataset and image folder
data = st.session_state.data
image_folder = st.session_state.image_folder

# Check if all questions have been answered
if not st.session_state.remaining_indices and st.session_state.current_index is None:
    st.write(f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
    st.stop()

# Get current question details
current_row = data.iloc[st.session_state.current_index]
image_path = os.path.join(image_folder, current_row["data_path"])

# Display the question image
st.title(f"{st.session_state.language} Quiz for {st.session_state.username}")
st.image(Image.open(image_path), use_container_width=True)

# Answer choices
options = ["A", "B", "C", "D"]
user_choice = st.radio("Select an answer:", options, key=st.session_state.current_index)

# Buttons for submitting or skipping
col1, col2 = st.columns(2)

def save_response(answer):
    """Save user response to the CSV file."""
    global responses_df
    new_row = pd.DataFrame([{
        "username": st.session_state.username,
        "language": st.session_state.language,
        "image_id": current_row["image_id"],
        "user_answer": answer
    }])
    responses_df = pd.concat([responses_df, new_row], ignore_index=True)
    responses_df.to_csv(RESPONSES_FILE, index=False)

with col1:
    if st.button("Next Question"):
        save_response(user_choice)
        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            st.session_state.current_index = None
            st.write(f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            st.stop()

with col2:
    if st.button("Skip Question"):
        save_response(np.nan)
        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            st.session_state.current_index = None
            st.write(f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            st.stop()