import streamlit as st
from textblob import TextBlob

# Set page config
st.set_page_config(page_title="Emotion Detector", page_icon="🙂", layout="centered")

# Fun emojis and colors
emotion_map = {
    "Very Positive": {"emoji": "😄", "color": "#D1FAE5"},  # light green
    "Positive": {"emoji": "🙂", "color": "#E0F7FA"},       # light blue
    "Neutral": {"emoji": "😐", "color": "#F3F4F6"},        # gray
    "Negative": {"emoji": "🙁", "color": "#FFF3CD"},       # light yellow
    "Very Negative": {"emoji": "😢", "color": "#F8D7DA"},  # light red
}

# Header
st.markdown("<h1 style='text-align: center;'>💬 Emotion Detector</h1>", unsafe_allow_html=True)
st.markdown("Enter any text and I’ll guess the emotion behind it! 🔍")

# Text input
user_input = st.text_area("Write something you're feeling...")

if user_input:
    # Analyze sentiment
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    # Decide emotion
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
    bg_color = emotion_map[emotion]["color"]

    # Show result with styled card
    st.markdown(
        f"""
        <div style="background-color:{bg_color}; padding: 1.2em; border-radius: 10px; text-align:center">
            <h2>{emoji} {emotion}</h2>
            <p><strong>Polarity Score:</strong> {round(polarity, 2)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Toast message (instant feedback)
    st.toast(f"Emotion: {emotion} {emoji}")

    # Optional: Show full sentiment object
    with st.expander("See full sentiment analysis"):
        st.json(blob.sentiment)
