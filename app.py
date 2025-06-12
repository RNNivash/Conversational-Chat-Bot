import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    return chat.send_message(question, stream=True)

# Streamlit UI Configuration
st.set_page_config(page_title="Conversational Chat Bot", layout="wide")
st.title("🤖 Conversational Chat Bot")
st.caption("© Nivash R N | 2025")

# Session state to preserve chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Layout: Two columns – Left (Response), Right (History)
col1, col2 = st.columns([2, 1])

# Input box and button
with col1:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your question:", placeholder="Ask me anything...")
        submitted = st.form_submit_button("🚀 Send")

    if submitted and user_input:
        # Add user input first to history
        st.session_state.chat_history.append(("You", user_input.strip()))

        response = get_gemini_response(user_input)
        bot_response = ""
        for chunk in response:
            bot_response += chunk.text

        # Clean up bot response
        clean_response = bot_response.strip().lstrip(".").replace("\n\n", "\n").strip()
        st.session_state.chat_history.append(("Bot", clean_response))

        with st.expander("🤖 Bot's Response", expanded=True):
            st.write(clean_response)

# Chat History (right column)
with col2:
    st.markdown("### 💬 Chat History")
    for i in range(0, len(st.session_state.chat_history), 2):
        user = st.session_state.chat_history[i]
        bot = st.session_state.chat_history[i + 1] if i + 1 < len(st.session_state.chat_history) else None

        # You: Display as styled bubble
        st.markdown(
            f"""
            <div style='background-color:#E3F2FD;padding:10px 15px;border-radius:10px;margin-bottom:5px'>
            <b style='color:#1565C0;'>You:</b><br>{user[1]}
            </div>
            """, unsafe_allow_html=True
        )

        # Bot: Display in green with markdown rendering (supports code blocks)
        if bot:
            with st.container():
                st.markdown(
                    f"""
                    <div style='background-color:#E8F5E9;padding:10px 15px;border-radius:10px;margin-bottom:20px'>
                    <b style='color:#2E7D32;'>Bot:</b>
                    </div>
                    """, unsafe_allow_html=True
                )
                st.markdown(bot[1])  # Render markdown like code blocks or lists