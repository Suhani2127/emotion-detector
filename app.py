import streamlit as st
from textblob import TextBlob

# ---------- Page Config ----------
st.set_page_config(page_title="AI Emotion Therapist", page_icon="🧠", layout="centered")

# ---------- Emotion Styling ----------
emotion_map = {
    "Very Positive": {
        "emoji": "😄",
        "color": "#f0fff4",  # very light green
        "response": "That’s amazing! Keep embracing those joyful moments! 🌟"
    },
    "Positive": {
        "emoji": "🙂",
        "color": "#f0faff",  # very light blue
        "response": "Glad to hear you're feeling good today! Keep going 💪"
    },
    "Neutral": {
        "emoji": "😐",
        "color": "#fafafa",  # light neutral gray
        "response": "It’s okay to feel neutral sometimes. Take a breath and keep moving 💫"
    },
    "Negative": {
        "emoji": "🙁",
        "color": "#fff9e6",  # soft yellow
        "response": "It’s okay to feel low. You’re not alone in this ❤️"
    },
    "Very Negative": {
        "emoji": "😢",
        "color": "#fff0f0",  # soft pink
        "response": "I'm really sorry you're feeling this way. Please be kind to yourself 🫂"
    }
}

# ---------- Custom Styles ----------
st.markdown(
    """
    <style>
    html, body, .main {
        background-color: white !important;
        font-family: 'Segoe UI', sans-serif;
        color: #222;
    }
    .title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #111;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtext {
        text-align: center;
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Header ----------
st.markdown("<div class='title'>🧠 AI Emotion Therapist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Tell me how you're feeling — I’ll respond with empathy and warmth 💖</div>", unsafe_allow_html=True)

# ---------- Text Input ----------
user_input = st.text_area("💬 Type your feelings here:")

# ---------- Logic & Output ----------
if user_input:
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        emotion = "Very Positive"
    elif polarity > 0:
        emotion = "Positive"
    elif polarity == 0:
        emotion = "Neutral"
    elif polarity > -0.5:
        emotion = "Negative"
    else:
        emotion = "Very Negative"

    emoji = emotion_map[emotion]["emoji"]
    color = emotion_map[emotion]["color"]
    response = emotion_map[emotion]["response"]

    st.markdown(
        f"""
        <div style='background-color:{color}; padding: 1.5rem; border-radius: 16px; text-align:center; border: 1px solid #ddd;'>
            <h2 style='color:#111;'>{emoji} {emotion}</h2>
            <p style='color:#333;'><strong>Polarity:</strong> {round(polarity, 2)}</p>
            <hr style='border: none; height: 1px; background-color: #ccc;' />
            <p style='font-size: 1.1rem; color:#222;'>{response}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.toast(f"{emoji} Emotion Detected: {emotion}")
