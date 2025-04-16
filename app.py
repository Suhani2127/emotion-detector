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

# Therapist personas based on emotions
therapist_personas = {
    "joy": "The Optimist",
    "love": "The Caregiver",
    "surprise": "The Explorer",
    "anger": "The Challenger",
    "sadness": "The Empath",
    "fear": "The Guide"
}

# -------------------------------
# Wellness Tips Based on Emotions
# -------------------------------
wellness_tips = {
    "joy": "Keep the positivity flowing! Take some time to appreciate the little things and keep nurturing your joy.",
    "love": "Spread the love! Practice acts of kindness and nurture your relationships with loved ones.",
    "surprise": "Embrace the unknown! When life surprises you, try to find the opportunities in it.",
    "anger": "Release your tension. Take deep breaths, meditate, or find a physical activity that helps you channel your anger.",
    "sadness": "Take it slow. Allow yourself to grieve and be kind to yourself. Journaling or talking to a friend might help.",
    "fear": "Breathe deeply. Acknowledge your fears, but remember that you have the strength to face them."
}

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
    animation: fall linear infinite;
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
    for word in ["sad", "happy", "tired", "anxious", "hopeful", "angry", "excited", "lonely"]:
        text = re.sub(f"\\b{word}\\b", f"**:blue[{word}]**", text, flags=re.IGNORECASE)
    return text

def emotion_therapist():
    st.markdown("<h2 style='text-align:center;'>🧠 AI Emotion Therapist</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tell me how you're feeling — I’ll respond with empathy 💖</p>", unsafe_allow_html=True)

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

        # Wellness Tip
        st.markdown(f"### 🧘 Wellness Tip:")
        st.markdown(wellness_tips.get(emotion, "Take care of yourself, every step counts."))

        # Therapist Persona
        persona = therapist_personas.get(emotion, "The Listener")
        st.markdown(f"### Therapist Persona: **{persona}**")
        
        today = datetime.date.today().strftime("%Y-%m-%d")
        username = st.session_state.get("username", "default")
        if username not in st.session_state["emotion_history"]:
            st.session_state["emotion_history"][username] = {}
        st.session_state["emotion_history"][username][today] = emotion

        st.markdown("---")
        st.subheader("💬 AI Therapist Says:")
        st.info(f"**{persona}:** {random.choice([f'Tell me more about that...', f'What do you think is causing this feeling?', 'I’m here to listen and support you.', 'It’s okay to feel this way, you’re not alone.'])}")

        # Journal Section
        st.markdown("---")
        st.subheader("📓 Journal Entry")
        journal = st.text_area("Write a short journal entry to reflect on your thoughts:")
        if st.button("Save Journal"):
            if username not in st.session_state["journal_entries"]:
                st.session_state["journal_entries"][username] = {}
            st.session_state["journal_entries"][username][today] = journal
            st.success("Journal entry saved!")
        
        # View Emotion History
        st.markdown("---")
        st.subheader("📅 Emotion History")
        if username in st.session_state["emotion_history"]:
            history = st.session_state["emotion_history"][username]
            history_df = pd.DataFrame(list(history.items()), columns=["Date", "Emotion"])
            st.dataframe(history_df)

if not st.session_state["logged_in"]:
    login_page()
else:
    emotion_therapist()

