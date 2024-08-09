import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
from audio_recorder_streamlit import audio_recorder
import io
import base64
from google.cloud import speech_v1p1beta1 as speech
from gtts import gTTS
import tempfile

# Load the environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini Voice Chatbot",
    layout="centered",
    page_icon="🧠"
)

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #FAF3E0; /* Warmer background color */
    }
    .title {
        color: lightskyblue; /* Lighter text color */
        font-size: 45px;
        text-align: center;
        font-family: verdana;
    }
    .user-message {
        background-color: #cce5ff; /* Light blue background for user messages */
        color: #003366; /* Dark blue text color */
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .assistant-message {
        background-color: #e6ffe6; /* Light green background for assistant messages */
        color: #004d00; /* Dark green text color */
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
    <h1><p class="title">🤔<b><i> Gemini AI Voice Chatbot</i></b> 🤔</p></h1>
    """,
    unsafe_allow_html=True
)

# Initialize the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up and define the Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Initialize Google Cloud Speech-to-Text client
def transcribe_audio(audio_data):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Initialize the chat session and welcome message in session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = []
    st.session_state.first_interaction = True  # Track if it's the first interaction
    st.session_state.welcome_displayed = False  # Track if the welcome message has been displayed

# Display the chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant" and not st.session_state.first_interaction:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Send the welcome message only for the first interaction
if st.session_state.first_interaction and not st.session_state.welcome_displayed:
    welcome_message = "Hello! Welcome to Gemini Chatbot! How may I help you today?"
    
    # Print the welcome message first
    st.markdown(f'<div class="assistant-message">{welcome_message}</div>', unsafe_allow_html=True)

    # Generate and play welcome message audio
    tts = gTTS(text=welcome_message, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
    
    # Append the welcome message after displaying it
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.first_interaction = False
    st.session_state.welcome_displayed = True

# Voice input button
st.write("Record your message:")
audio_data = audio_recorder()

if audio_data:
    st.write("Processing audio...")
    # Convert audio to base64 and pass to Google Cloud Speech-to-Text
    audio_bytes = base64.b64decode(audio_data)
    user_prompt = transcribe_audio(audio_bytes)
    st.write(f"You said: {user_prompt}")
    
    # Add user's question to chat and display it
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.markdown(f'<div class="user-message">{user_prompt}</div>', unsafe_allow_html=True)

    # Send user's question to Gemini-Pro and get answer
    gemini_answer = st.session_state.chat_session.send_message(user_prompt)

    # Display and voice the answer
    st.session_state.messages.append({"role": "assistant", "content": gemini_answer.text})
    st.markdown(f'<div class="assistant-message">{gemini_answer.text}</div>', unsafe_allow_html=True)

    # Generate and play answer audio
    tts = gTTS(text=gemini_answer.text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
