import streamlit as st
from textblob import TextBlob

# ---------- Config ----------
st.set_page_config(page_title="AI Emotion Therapist", page_icon="🧠", layout="centered")

# ---------- Emotion Map ----------
emotion_map = {
    "Very Positive": {
        "emoji": "😄",
        "color": "#d1ffd6",
        "response": "That’s amazing! Keep embracing those joyful moments! 🌟"
    },
    "Positive": {
        "emoji": "🙂",
        "color": "#e0f4ff",
        "response": "Glad to hear you're feeling good today! Keep going 💪"
    },
    "Neutral": {
        "emoji": "😐",
        "color": "#f0f0f0",
        "response": "It’s okay to feel neutral sometimes. Take a breath and keep moving 💫"
    },
    "Negative": {
        "emoji": "🙁",
        "color": "#fff3cd",
        "response": "It’s okay to feel low. You’re not alone in this ❤️"
    },
    "Very Negative": {
        "emoji": "😢",
        "color": "#ffe0e0",
        "response": "I'm really sorry you're feeling this way. Please be kind to yourself 🫂"
    }
}

# ---------- UI Styling ----------
st.markdown(
    """
    <style>
    .main {
        font-family: 'Segoe UI', sans-serif;
        background-color: #ffffff;
        padding: 2rem;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #111;
    }
    .subtext {
        text-align: center;
        font-size: 1rem;
        color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Title ----------
st.markdown("<div class='title'>🧠 AI Emotion Therapist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Tell me how you're feeling. I’ll respond with empathy 💖</div>", unsafe_allow_html=True)

# ---------- Text Input ----------
user_input = st.text_area("💬 Type something you're feeling:")

if user_input:
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    # Determine emotion
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

    # ---------- Emotion Card ----------
    st.markdown(
        f"""
        <div style='background-color:{color}; padding: 1.5rem; border-radius: 12px; text-align:center;'>
            <h2 style='color:#000;'>{emoji} {emotion}</h2>
            <p style='color:#000;'><strong>Polarity:</strong> {round(polarity, 2)}</p>
            <hr style='border: none; height: 1px; background-color: #ccc;' />
            <p style='font-size: 1.1rem; color:#000;'>{response}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.toast(f"{emoji} Emotion Detected: {emotion}")
