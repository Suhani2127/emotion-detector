import streamlit as st
from transformers import pipeline
import datetime
import random
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

# -------------------------------
# Emotion Classifier with Hugging Face
# -------------------------------
emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion", return_all_scores=True)

# -------------------------------
# Dummy credentials (in-memory)
# -------------------------------
if "users" not in st.session_state:
    st.session_state["users"] = {"admin": "1234"}  # default user

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "emotion_history" not in st.session_state:
    st.session_state["emotion_history"] = {}

if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = {}

# -------------------------------
# Emotion Analysis Logic
# -------------------------------
def get_emotion(text):
    scores = emotion_classifier(text)[0]
    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    top_emotion = sorted_scores[0]['label']
    top_score = sorted_scores[0]['score']
    return top_emotion.capitalize(), top_score

emotion_map = {
    "Joy": {"emoji": "😊", "color": "#E0F7FA", "response": "That’s wonderful to hear! 🌟 What made you feel joyful today?"},
    "Sadness": {"emoji": "😢", "color": "#F8D7DA", "response": "I'm really sorry you're feeling this way. Do you want to talk about it?"},
    "Anger": {"emoji": "😠", "color": "#FFE0B2", "response": "It's okay to feel angry. Would you like to vent or find ways to calm down?"},
    "Love": {"emoji": "❤️", "color": "#FCE4EC", "response": "Love is such a beautiful emotion. Tell me more!"},
    "Fear": {"emoji": "😨", "color": "#FFF3CD", "response": "It's natural to feel fear. You are safe here."},
    "Surprise": {"emoji": "😮", "color": "#E1F5FE", "response": "Surprises can be exciting or shocking. What happened?"}
}

therapist_replies = [
    "Tell me more about that...",
    "How long have you been feeling this way?",
    "What do you think is causing this feeling?",
    "That's a valid feeling. What have you done to cope with it so far?",
    "Would you like to talk about something that made you feel better before?",
    "You're not alone in this. I'm here for you."
]

highlight_keywords = ["sad", "happy", "tired", "anxious", "hopeful", "angry", "excited", "lonely"]

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
html, body, .main {
    background-color: white;
    color: #111;
    font-family: 'Segoe UI', sans-serif;
}
textarea, input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Auth Page
# -------------------------------
def login_page():
    st.title("🔐 Login to AI Emotion Therapist")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state["users"] and st.session_state["users"][username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully ✅")
        else:
            st.error("Invalid credentials ❌")

    st.markdown("---")
    st.subheader("New here? Sign up below:")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_user in st.session_state["users"]:
            st.warning("Username already taken.")
        else:
            st.session_state["users"][new_user] = new_pass
            st.success("Account created! You can now log in.")

# -------------------------------
# Emotion Therapist Page
# -------------------------------
def highlight_text(text):
    for word in highlight_keywords:
        text = re.sub(f"\\b{word}\\b", f"**:blue[{word}]**", text, flags=re.IGNORECASE)
    return text

def emotion_therapist():
    st.markdown("<h2 style='text-align:center;'>🧠 AI Emotion Therapist</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tell me how you're feeling — I’ll respond with empathy 💖</p>", unsafe_allow_html=True)

    user_input = st.text_area("💬 How are you feeling today?")
    if user_input:
        emotion, score = get_emotion(user_input)
        info = emotion_map.get(emotion, {"emoji": "🤔", "color": "#F4F4F4", "response": "I'm thinking about how you're feeling..."})

        st.markdown(f"""
            <div style='background-color:{info['color']}; padding: 1.5rem; border-radius: 16px; text-align:center; border: 1px solid #bbb;'>
                <h2 style='color:#111;'>{info['emoji']} {emotion}</h2>
                <p><strong>Confidence:</strong> {round(score * 100, 2)}%</p>
                <hr />
                <p style='font-size: 1.1rem;'>{info['response']}</p>
            </div>
        """, unsafe_allow_html=True)

        st.toast(f"{info['emoji']} Emotion Detected: {emotion}")

        today = datetime.date.today().strftime("%Y-%m-%d")
        username = st.session_state.get("username", "default")
        if username not in st.session_state["emotion_history"]:
            st.session_state["emotion_history"][username] = {}
        st.session_state["emotion_history"][username][today] = emotion

        st.markdown("---")
        st.subheader("💬 AI Therapist Says:")
        st.info(random.choice(therapist_replies))

        # Journal Section
        st.markdown("---")
        st.subheader("📓 Journal Entry")
        journal = st.text_area("Write a short journal entry to reflect on your thoughts:")
        if st.button("Save Journal"):
            if username not in st.session_state["journal_entries"]:
                st.session_state["journal_entries"][username] = {}
            st.session_state["journal_entries"][username][today] = {
                "text": journal,
                "emotion": emotion
            }
            st.success("Journal saved successfully ✨")

    st.markdown("---")
    st.subheader("📅 Your Emotion History")

    selected_date = st.date_input("Pick a date to view past emotion")
    username = st.session_state.get("username", "default")
    history = st.session_state["emotion_history"].get(username, {})
    date_str = selected_date.strftime("%Y-%m-%d")

    if date_str in history:
        past_emotion = history[date_str]
        past_info = emotion_map.get(past_emotion, {"emoji": "🤔", "color": "#EEE"})
        st.markdown(f"**{date_str}:** {past_info['emoji']} {past_emotion}")

        journal_entries = st.session_state["journal_entries"].get(username, {})
        if date_str in journal_entries:
            st.markdown("---")
            st.markdown("### 📝 Journal Reflection:")
            highlighted = highlight_text(journal_entries[date_str]["text"])
            st.markdown(highlighted)
    else:
        st.info("No emotion entry recorded for this date.")

    # Heatmap
    if history:
        st.markdown("---")
        st.subheader("📈 Monthly Emotion Heatmap")

        df = pd.DataFrame(list(history.items()), columns=["Date", "Emotion"])
        df["Date"] = pd.to_datetime(df["Date"])
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Emotion Level"] = df["Emotion"].map({
            "Sadness": -2,
            "Fear": -1,
            "Neutral": 0,
            "Joy": 2,
            "Anger": -1,
            "Surprise": 1,
            "Love": 2
        })

        heatmap_data = df.pivot_table(index="Month", columns="Day", values="Emotion Level")
        plt.figure(figsize=(15, 3))
        sns.heatmap(heatmap_data, cmap="coolwarm", cbar_kws={'label': 'Emotion Intensity'}, linewidths=0.5, linecolor='white')
        st.pyplot(plt)

    if st.button("🔓 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

# -------------------------------
# Main App Flow
# -------------------------------
if not st.session_state["logged_in"]:
    login_page()
else:
    emotion_therapist()

