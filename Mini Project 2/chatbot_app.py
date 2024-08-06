import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os

# Load the environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini Chatbot",
    layout="centered",
    page_icon="🧠" 
)

# Apply custom CSS to change text color
st.markdown(
    """
    <style>
    .title {
        color: white;  
        font-size: 40px; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up and define the Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Create a function to translate roles between Gemini-Pro and Streamlit terminology
def translate_roles(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

# Initialize a chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page with custom styling
#st.markdown('<h1><p class="title">🤔Gemini API Chatbot🤔</p></h1>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .title {
        color: teal;
        font-size: 45px;
        text-align: center;
        font-family:verdana;
    }
    </style>
    <h1><p class="title">🤔<b><i> Gemini API Chatbot</i></b> 🤔</p></h1>
    """,
    unsafe_allow_html=True
)


# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_roles(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user input
user_prompt = st.chat_input("Enter your prompt...")
if user_prompt:
    # Add user's question to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's question to Gemini-Pro and get answer
    gemini_answer = st.session_state.chat_session.send_message(user_prompt)

    # Display the answer on the screen
    with st.chat_message("assistant"):
        st.markdown(gemini_answer.text)
