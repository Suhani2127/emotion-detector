import streamlit as st
from textblob import TextBlob
import datetime

# -------------------------------
# Dummy credentials (in-memory)
# -------------------------------
if "users" not in st.session_state:
    st.session_state["users"] = {"admin": "1234"}  # default user

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "emotion_history" not in st.session_state:
    st.session_state["emotion_history"] = {}

# -------------------------------
# Emotion Analysis Logic
# -------------------------------
def get_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif polarity > 0:
        return "Positive", polarity
    elif polarity == 0:
        return "Neutral", polarity
    elif polarity > -0.5:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

emotion_map = {
    "Very Positive": {"emoji": "😄", "color": "#f0fff4", "response": "That’s amazing! Keep embracing those joyful moments! 🌟"},
    "Positive": {"emoji": "🙂", "color": "#f0faff", "response": "Glad to hear you're feeling good today! Keep going 💪"},
    "Neutral": {"emoji": "😐", "color": "#fafafa", "response": "It’s okay to feel neutral sometimes. Take a breath and keep moving 💫"},
    "Negative": {"emoji": "🙁", "color": "#fff9e6", "response": "It’s okay to feel low. You’re not alone in this ❤️"},
    "Very Negative": {"emoji": "😢", "color": "#fff0f0", "response": "I'm really sorry you're feeling this way. Please be kind to yourself 🫂"}
}

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
html, body, .main {
    background-color: white;
    color: #222;
    font-family: 'Segoe UI', sans-serif;
}
textarea {
    background-color: #fff !important;
    color: #000 !important;
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
def emotion_therapist():
    st.markdown("<h2 style='text-align:center;'>🧠 AI Emotion Therapist</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tell me how you're feeling — I’ll respond with empathy 💖</p>", unsafe_allow_html=True)

    user_input = st.text_area("💬 How are you feeling today?")
    if user_input:
        emotion, polarity = get_emotion(user_input)
        info = emotion_map[emotion]

        st.markdown(f"""
            <div style='background-color:{info['color']}; padding: 1.5rem; border-radius: 16px; text-align:center; border: 1px solid #ddd;'>
                <h2 style='color:#111;'>{info['emoji']} {emotion}</h2>
                <p><strong>Polarity:</strong> {round(polarity, 2)}</p>
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
    st.subheader("📅 Your Emotion History")

    selected_date = st.date_input("Pick a date to view past emotion")
    username = st.session_state.get("username", "default")
    history = st.session_state["emotion_history"].get(username, {})
    date_str = selected_date.strftime("%Y-%m-%d")

    if date_str in history:
        past_emotion = history[date_str]
        past_info = emotion_map[past_emotion]
        st.markdown(f"**{date_str}:** {past_info['emoji']} {past_emotion}")
    else:
        st.info("No emotion entry recorded for this date.")

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
