import streamlit as st
import random
import datetime

# Emotion mapping for displaying response
emotion_map = {
    "happy": {"emoji": "😊", "color": "#FFFF00", "response": "That's wonderful! Keep smiling."},
    "sad": {"emoji": "😢", "color": "#00BFFF", "response": "I'm sorry you're feeling down. It will get better."},
    "angry": {"emoji": "😡", "color": "#FF4500", "response": "Take a deep breath. It’s okay to feel frustrated."},
    "neutral": {"emoji": "😐", "color": "#808080", "response": "It’s okay to feel neutral. You’re doing well."},
    "fear": {"emoji": "😨", "color": "#FFD700", "response": "It’s okay to feel scared. Try to relax and breathe."},
    "surprised": {"emoji": "😲", "color": "#00FF00", "response": "Life can surprise us! Embrace it."},
    "disgust": {"emoji": "🤢", "color": "#FF6347", "response": "It’s normal to feel disgust. Let it pass."},
}

# Sample therapist replies
therapist_replies = [
    "You're doing great, remember to be kind to yourself.",
    "It's okay to feel this way. Take your time.",
    "Feelings are valid, embrace them with compassion.",
    "Everything will get better soon, stay strong!"
]

# Function to detect emotion (Dummy function for now)
def get_emotion(user_input):
    # This function will return emotion and confidence score based on user input
    # For the sake of this example, let's randomly choose an emotion
    emotions = list(emotion_map.keys())
    emotion = random.choice(emotions)
    score = round(random.uniform(0.7, 1.0), 2)
    return emotion, score

# Highlight important words in journal text (Dummy function for now)
def highlight_text(text):
    # Add simple highlighting (e.g., bold)
    return text.replace("important", "**important**").replace("remember", "**remember**")

# Main emotion therapist function
def emotion_therapist():
    st.markdown("<h2 style='text-align:center;'>🧠 AI Emotion Therapist</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tell me how you're feeling — I’ll respond with empathy 💖</p>", unsafe_allow_html=True)

    # Adding a unique key to the text area widget for user input
    user_input = st.text_area("💬 How are you feeling today?", key="user_input_1")
    
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

        st.toast(f"{info['emoji']} Emotion Detected: {emotion}")

        today = datetime.date.today().strftime("%Y-%m-%d")
        username = st.session_state.get("username", "default")
        if username not in st.session_state["emotion_history"]:
            st.session_state["emotion_history"][username] = {}
        st.session_state["emotion_history"][username][today] = emotion

        st.markdown("---")
        st.subheader("💬 AI Therapist Says:")
        st.info(random.choice(therapist_replies))

        # Journal Section with unique key for text area
        st.markdown("---")
        st.subheader("📓 Journal Entry")
        journal = st.text_area("Write a short journal entry to reflect on your thoughts:", key="journal_entry_1")
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

# Ensure these variables are initialized before usage
if "emotion_history" not in st.session_state:
    st.session_state["emotion_history"] = {}

if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = {}

# Run the emotion therapist function
emotion_therapist()

