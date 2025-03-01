import streamlit as st
import os
import random
import pandas as pd
import numpy as np
from PIL import Image

# Define CSV files and image folders for different languages
CSV_FILES = {
    "Yoruba": "data/YOR/2010/2010.csv",  # Change to actual file paths
    "Igbo": "data/igbo_questions/IGBO.csv"  # Change to actual file paths
}
IMAGE_FOLDERS = {
    "Yoruba": "2010/",  # Change to actual folder paths
    "Igbo": "data/igbo_questions"  # Change to actual folder paths
}

# Initialize session state for user details, language selection, questions, and answers
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
    username = st.text_input("Enter your name to start:")
    language = st.selectbox("Select a language:", [
                            "Yoruba", "Igbo"], index=None, placeholder="Choose...")

    if st.button("Start Quiz") and username and language:
        st.session_state.username = username
        st.session_state.language = language
        data = pd.read_csv(CSV_FILES[language])
        st.session_state.data = data  # Store the selected dataset in session state
        # Store the selected image folder
        st.session_state.image_folder = IMAGE_FOLDERS[language]
        st.session_state.remaining_indices = list(range(len(data)))
        random.shuffle(st.session_state.remaining_indices)
        st.session_state.current_index = st.session_state.remaining_indices.pop()
        st.rerun()
    st.stop()

# Load the selected language dataset and image folder
data = st.session_state.data
image_folder = st.session_state.image_folder

# Check if all questions have been answered
if not st.session_state.remaining_indices and "current_index" not in st.session_state:
    st.write(
        f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
    # Convert user answers to a DataFrame and display it
    answers_df = pd.DataFrame(st.session_state.user_answers)
    st.write("Your responses:")
    st.dataframe(answers_df)
    st.stop()

# Get current question details
current_row = data.iloc[st.session_state.current_index]
image_path = os.path.join(image_folder, current_row["data_path"])

# Display the question image
st.title(f"{st.session_state.language} Quiz for {st.session_state.username}")
st.image(Image.open(image_path), use_container_width=True)

# Answer choices
options = ["A", "B", "C", "D"]
user_choice = st.radio("Select an answer:", options,
                       key=st.session_state.current_index)


# Buttons to submit answer or skip
col1, col2 = st.columns(2)
with col1:
    if st.button("Next Question"):
        # Store user response
        st.session_state.user_answers.append({
            "username": st.session_state.username,
            "language": st.session_state.language,
            "image_id": current_row["image_id"],
            "user_answer": user_choice
        })

        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            del st.session_state.current_index  # Remove current question to stop rerunning
            st.write(
                f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            answers_df = pd.DataFrame(st.session_state.user_answers)
            st.write("Your responses:")
            st.dataframe(answers_df)
            st.stop()

with col2:
    if st.button("Skip Question"):
        # Store skipped response as NaN
        st.session_state.user_answers.append({
            "username": st.session_state.username,
            "language": st.session_state.language,
            "image_id": current_row["image_id"],
            "user_answer": np.nan
        })

        if st.session_state.remaining_indices:
            st.session_state.current_index = st.session_state.remaining_indices.pop()
            st.rerun()
        else:
            del st.session_state.current_index  # Remove current question to stop rerunning
            st.write(
                f"Thank you for participating, {st.session_state.username}! Goodbye! 👋")
            answers_df = pd.DataFrame(st.session_state.user_answers)
            st.write("Your responses:")
            st.dataframe(answers_df)
            st.stop()
