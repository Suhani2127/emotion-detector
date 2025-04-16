import streamlit as st
from textblob import TextBlob
import datetime
import random
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
from transformers import pipeline
import openai

# Load advanced emotion classifier
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

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
    results = emotion_classifier(text)[0]
    results.sort(key=lambda x: x['score'], reverse=True)
    top = results[0]
    return top['label'], round(top['score'], 2)

emotion_map = {
    "joy": {"emoji": "😄", "color": "#DFF6E2", "response": "That’s amazing! Keep embracing those joyful moments! 🌟"},
    "love": {"emoji": "❤️", "color": "#FFE3E3", "response": "That’s lovely. Spread the love! 🌈"},
    "surprise": {"emoji": "😲", "color": "#E0F7FF", "response": "Surprises can be exciting or shocking! Let’s talk more."},
    "anger": {"emoji": "😠", "color": "#FFD6D6", "response": "It’s okay to feel angry. Let’s try to unpack that together."},
    "sadness": {"emoji": "😢", "color": "#F8D7DA", "response": "I'm really sorry you're feeling this way. Please be kind to yourself 🫂"},
    "fear": {"emoji": "😨", "color": "#EAEAFF", "response": "Fear is a powerful emotion. Let's work through it together."}
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
.emoji-rain {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    pointer-events: none;
    z-index: 9999;
}
.emoji-rain span {
    position: absolute;
    font-size: 3rem;
    animation: fall linear 5s;
    opacity: 1;
}
@keyframes fall {
    0% {
        transform: translateY(-100px) rotate(0deg);
        opacity: 1;
    }
    100% {
        transform: translateY(120vh) rotate(360deg);
        opacity: 0.8;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Therapist Personas
# -------------------------------
therapist_personas = {
    "Compassionate Counselor": "You are a compassionate counselor who always listens with empathy. You validate emotions gently and encourage self-kindness.",
    "Motivational Coach": "You are a high-energy motivational coach who uplifts users with inspiring words and helps them reframe challenges positively.",
    "Mindful Zen Guide": "You are a peaceful, Zen-like guide who helps users stay grounded through mindfulness, reflection, and breathing awareness.",
    "Cognitive-Behavioral Strategist": "You are a logical and supportive therapist using Cognitive Behavioral Therapy to help users challenge negative thoughts and build positive behaviors.",
    "Warm Best Friend": "You are a loving and understanding best friend who always knows what to say to comfort, cheer up, or support the user, no matter what."
}

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

    # Therapist Persona Selection
    if "persona" not in st.session_state:
        st.session_state.persona = "Compassionate Counselor"

    st.sidebar.subheader("🧑‍⚕️ Choose Your Therapist Persona")
    st.session_state.persona = st.sidebar.selectbox("Therapist Style", [
        "Compassionate Counselor",
        "Motivational Coach",
        "Mindful Zen Guide",
        "Cognitive-Behavioral Strategist",
        "Warm Best Friend"
    ])

    user_input = st.text_area("💬 How are you feeling today?")
    if user_input:
        emotion, score = get_emotion(user_input)
        info = emotion_map.get(emotion, {"emoji": "❓", "color": "#eee", "response": "I'm not sure how to categorize that emotion."})

        # Emoji Rain
        st.markdown(f"""
        <div class="emoji-rain">
            {''.join([f"<span style='left:{random.randint(0, 100)}vw; animation-duration: {random.uniform(2, 5)}s;'>{info['emoji']}</span>" for _ in range(50)])}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='background-color:{info['color']}; padding: 1.5rem; border-radius: 16px; text-align:center; border: 1px solid #bbb;'>
                <h2 style='color:#111;'>{info['emoji']} {emotion.capitalize()}</h2>
                <p><strong>Confidence:</strong> {score}</p>
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

# -------------------------------
# Main App Logic
# -------------------------------
if not st.session_state["logged_in"]:
    login_page()
else:
    emotion_therapist()

