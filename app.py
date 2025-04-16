import streamlit as st
from textblob import TextBlob

# ---------- Config ----------
st.set_page_config(page_title="AI Emotion Therapist", page_icon="🧠", layout="centered")

# ---------- Emotion Map ----------
emotion_map = {
    "Very Positive": {
        "emoji": "😄",
        "color": "#D1FAE5",
        "response": "That’s amazing! Keep embracing those joyful moments! 🌟"
    },
    "Positive": {
        "emoji": "🙂",
        "color": "#E0F7FA",
        "response": "Glad to hear you're feeling good today! Keep going 💪"
    },
    "Neutral": {
        "emoji": "😐",
        "color": "#F3F4F6",
        "response": "It’s okay to feel neutral sometimes. Take a breath and keep moving 💫"
    },
    "Negative": {
        "emoji": "🙁",
        "color": "#FFF3CD",
        "response": "It’s okay to feel low. You’re not alone in this ❤️"
    },
    "Very Negative": {
        "emoji": "😢",
        "color": "#F8D7DA",
        "response": "I'm really sorry you're feeling this way. Please be kind to yourself 🫂"
    }
}

# ---------- UI ----------
st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .subtext {
        text-align: center;
        font-size: 1rem;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🧠 AI Emotion Therapist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Tell me how you're feeling. I'll listen and respond with kindness.</div>", unsafe_allow_html=True)

# ---------- Text Input ----------
user_input = st.text_area("💬 Your message")

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
        <div style='background-color:{color}; padding: 1.5rem; border-radius: 12px; text-align:center;'>
            <h2>{emoji} {emotion}</h2>
            <p><strong>Polarity:</strong> {round(polarity, 2)}</p>
            <hr style='border: none; height: 1px; background-color: #ccc;' />
            <p style='font-size: 1.1rem;'>{response}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.toast(f"{emoji} Emotion Detected: {emotion}")
