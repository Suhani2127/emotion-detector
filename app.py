mport streamlit as st
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

mental_health_tips = {
    "joy": ["Savor the moment with gratitude journaling.", "Share your happiness with someone—it amplifies the feeling!"],
    "love": ["Send a kind message to someone you care about today.", "Practice self-love through affirmations or a relaxing activity."],
    "surprise": ["Take a moment to breathe—surprises can bring growth!", "Write down your feelings—it helps make sense of the unexpected."],
    "anger": ["Take a walk or do a quick stretch to release tension.", "Try deep breathing: inhale for 4, hold for 4, exhale for 6."],
    "sadness": ["Watch or listen to something that brings you comfort.", "Reach out to a friend or write down how you’re feeling."],
    "fear": ["Ground yourself with the 5-4-3-2-1 technique (see, hear, feel, smell, taste).", "Face fears gradually—small steps make a big impact."]
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
    animation: fall 4s linear infinite;
    font-size: 3rem;
    opacity: 0.95;
}
@keyframes fall {
    0% { transform: translateY(-100px); opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
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
        info = emotion_map.get(emotion, {"emoji": "❓", "color": "#eee", "response": "I'm not sure how to categorize that emotion."})

        # Emoji Rain
        st.markdown(f"""
        <div class="emoji-rain">
            {''.join([f"<span style='left:{random.randint(0, 100)}vw'>{info['emoji']}</span>" for _ in range(80)])}
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

        # Mental health tips
        if emotion in mental_health_tips:
            st.markdown("---")
            st.subheader("🧘 Mental Health Tip:")
            st.success(random.choice(mental_health_tips[emotion]))

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
        past_info = emotion_map.get(past_emotion, {"emoji": "❓"})
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
            "sadness": -2,
            "anger": -1,
            "fear": -1,
            "surprise": 0,
            "love": 1,
            "joy": 2
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

