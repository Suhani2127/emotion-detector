import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Emotion Detector", page_icon="🙂")
st.title("Emotion Detector from Text")
st.write("Type anything below and see the emotion behind it!")

user_input = st.text_area("Enter your text here:")

if user_input:
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        emotion = "Very Positive 😊"
    elif polarity > 0:
        emotion = "Positive 🙂"
    elif polarity == 0:
        emotion = "Neutral 😐"
    elif polarity > -0.5:
        emotion = "Negative 🙁"
    else:
        emotion = "Very Negative 😢"

    st.subheader("Detected Emotion:")
    st.markdown(f"**{emotion}** (polarity score: {round(polarity, 2)})")
