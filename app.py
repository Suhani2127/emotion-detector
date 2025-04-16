import streamlit as st
from textblob import TextBlob

# -------------------------------
# Dummy credentials (in-memory)
# -------------------------------
if "users" not in st.session_state:
    st.session_state["users"] = {"admin": "1234"}  # default user

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# -------------------------------
# Emotion Analysis Logic
# -------------------------------
def get_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", 0.5
    elif polarity > 0:
        return "Positive", 0.2
    elif polarity == 0:
        return "Neutral", 0.0
    elif polarity > -0.5:
        return "Negative", -0.2
    else:
        return "Very Negative", -0.5

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
