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

# Meditation Options Based on Emotion
def suggest_meditation(emotion):
    meditations = {
        "anger": {
            "title": "Calming Breathing Meditation",
            "link": "https://www.youtube.com/watch?v=Jyy0LZJgUBg"  # Placeholder link
        },
        "fear": {
            "title": "Overcoming Fear Guided Meditation",
            "link": "https://www.youtube.com/watch?v=dyEJbtz7h-8"  # Placeholder link
        },
        "sadness": {
            "title": "Healing from Sadness Meditation",
            "link": "https://www.youtube.com/watch?v=7BzKckTbVZk"  # Placeholder link
        },
        "joy": {
            "title": "Gratitude Meditation",
            "link": "https://www.youtube.com/watch?v=xdFjhr2Vd2M"  # Placeholder link
        },
        "love": {
            "title": "Loving Kindness Meditation",
            "link": "https://www.youtube.com/watch?v=w2YjFjxWGG8"  # Placeholder link
        }
    }
    return meditations.get(emotion, {"title": "Meditation Session", "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})  # Default to a meditation link

# Display Meditation Suggestion Based on Emotion
def display_meditation(emotion):
    meditation = suggest_meditation(emotion)
    st.markdown(f"### Recommended Meditation: {meditation['title']}")
    st.markdown(f"[Click here to start meditation]({meditation['link']})")
# Affirmations Based on Emotion
def get_affirmation(emotion):
    affirmations = {
        "anger": "I choose to release the need for anger and allow peace to enter.",
        "fear": "I am safe, I am capable, and I am resilient.",
        "sadness": "This too shall pass, and I will emerge stronger.",
        "joy": "I embrace happiness and let it fill my heart with positivity.",
        "love": "I am deserving of love and kindness.",
    }
    return affirmations.get(emotion, "I am in control of my emotions and my future.")

# Display Affirmation Based on Emotion
def display_affirmation(emotion):
    affirmation = get_affirmation(emotion)
    st.markdown(f"### Affirmation: {affirmation}")
# Manage Emergency Contacts
def manage_emergency_contacts():
    st.markdown("### Emergency Contacts")

    # If this is the user's first time adding contacts, initialize the contacts dictionary
    if "emergency_contacts" not in st.session_state:
        st.session_state["emergency_contacts"] = []

    # Add new contact
    new_contact = st.text_input("Add a New Emergency Contact (Name and Phone Number)")
    if st.button("Add Contact"):
        if new_contact:
            st.session_state["emergency_contacts"].append(new_contact)
            st.success(f"Emergency contact '{new_contact}' added successfully.")
        else:
            st.warning("Please enter a contact.")

    # Display existing contacts
    if st.session_state["emergency_contacts"]:
        st.write("### Your Emergency Contacts:")
        for contact in st.session_state["emergency_contacts"]:
            st.markdown(f"- {contact}")
    else:
        st.write("No emergency contacts added yet.")

# -----------------------------
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

        # Wellness Resources Section
        st.markdown("---")
        st.subheader("💆‍♀️ Wellness Resources")
        
        # Meditation Suggestion
        display_meditation(emotion)

        # Affirmation
        display_affirmation(emotion)

        # Emergency Contacts
        manage_emergency_contacts()

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

