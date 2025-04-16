import streamlit as st
import matplotlib.pyplot as plt
import calendar
import datetime
import random
import openai
from transformers import pipeline
import numpy as np

# Setup emotion classifier
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=3)

# Emoji mapping for emotions
emoji_map = {
    "anger": "😠",
    "disgust": "🤢",
    "fear": "😨",
    "joy": "😊",
    "sadness": "😢",
    "surprise": "😲",
    "neutral": "😐",
    "happy": "😄",
    "love": "❤️",
    "worry": "😟"
}

# Sample fallback responses
therapist_replies = [
    "I'm here for you. Would you like to talk more about it?",
    "That's completely valid. It's okay to feel that way.",
    "Let's try to take a deep breath together. In and out.",
    "What do you think triggered this emotion today?",
    "You're doing better than you think."
]

# Configure OpenAI key
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""
openai.api_key = st.session_state["openai_api_key"]

# Memory of user logins (simulated)
users = {"testuser": "password"}

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Storage for emotion history
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = {}

def login_page():
    st.title("🔐 Login to AI Emotion Therapist")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
    st.markdown("---")
    st.subheader("🔑 Enter OpenAI API Key (optional for advanced replies)")
    st.session_state["openai_api_key"] = st.text_input("API Key", type="password")

def get_emotion(text):
    try:
        results = emotion_classifier(text)[0]
        results.sort(key=lambda x: x['score'], reverse=True)
        top = results[0]
        return top['label'], round(top['score'], 2)
    except:
        return "unknown", 0.0

def generate_gpt_reply(user_input):
    if not openai.api_key:
        return random.choice(therapist_replies)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a kind and empathetic mental health therapist."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except:
        return random.choice(therapist_replies)

def emotion_therapist():
    st.title("🧠 AI Emotion Therapist")
    st.write("How are you feeling today?")
    user_input = st.text_area("Describe your mood or thoughts:")

    if st.button("Analyze Emotion"):
        if user_input:
            emotion, score = get_emotion(user_input)
            emoji = emoji_map.get(emotion.lower(), "❓")
            st.subheader(f"Detected Emotion: {emotion} {emoji} ({score})")

            # Save history
            today = datetime.date.today()
            st.session_state.emotion_history[str(today)] = emotion

            # GPT therapist reply
            st.subheader("💬 AI Therapist Says:")
            response = generate_gpt_reply(user_input)
            st.info(response)

            # Emoji explosion effect (rain across screen)
            st.markdown("""
                <style>
                .emoji-rain {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    z-index: 9999;
                    pointer-events: none;
                    overflow: hidden;
                }
                .emoji-rain span {
                    font-size: 3rem;
                    animation: fall 3s linear infinite;
                    position: absolute;
                    top: -10%;
                    opacity: 1;
                }
                @keyframes fall {
                    to {
                        transform: translateY(110vh);
                        opacity: 0;
                    }
                }
                </style>
                <div class="emoji-rain">
                """ + "".join([
                    f'<span style="left:{random.randint(0, 100)}vw">{emoji}</span>' for _ in range(30)
                ]) + "</div>", unsafe_allow_html=True)

def calendar_heatmap():
    st.title("📅 Emotion History")
    today = datetime.date.today()
    year = today.year
    month = today.month
    cal = calendar.monthcalendar(year, month)

    data = np.zeros((len(cal), 7))
    emotion_colors = {
        "joy": "#ffe066", "sadness": "#74c0fc", "anger": "#fa5252",
        "fear": "#7950f2", "surprise": "#63e6be", "neutral": "#dee2e6",
        "happy": "#ffd43b", "love": "#ff8787", "worry": "#ffa94d"
    }

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title(f"{calendar.month_name[month]} {year}", fontsize=16)
    ax.axis("off")

    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day != 0:
                date_str = str(datetime.date(year, month, day))
                emotion = st.session_state.emotion_history.get(date_str, "")
                color = emotion_colors.get(emotion, "#f1f3f5")
                rect = plt.Rectangle([j, -i], 1, 1, facecolor=color, edgecolor="white")
                ax.add_patch(rect)
                ax.text(j + 0.5, -i + 0.5, str(day), ha="center", va="center", fontsize=10)

    st.pyplot(fig)

def main():
    if not st.session_state.logged_in:
        login_page()
        return

    menu = ["Emotion Analyzer", "Calendar Heatmap", "Logout"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Emotion Analyzer":
        emotion_therapist()
    elif choice == "Calendar Heatmap":
        calendar_heatmap()
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()

if __name__ == "__main__":
    main()

