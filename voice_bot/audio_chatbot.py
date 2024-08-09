import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import tempfile
import google.auth
from google.cloud import speech_v1 as speech

# Load environment variables
load_dotenv()

# Set up Google API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["google"]["api_key"]
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

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
        background-color: #FAF3E0;
    }
    .title {
        color: lightskyblue;
        font-size: 45px;
        text-align: center;
        font-family: verdana;
    }
    .user-message {
        background-color: #cce5ff;
        color: #003366;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .assistant-message {
        background-color: #e6ffe6;
        color: #004d00;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
    <h1><p class="title">🤔<b><i> Gemini AI Voice Chatbot</i></b> 🤔</p></h1>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = []
    st.session_state.first_interaction = True
    st.session_state.welcome_displayed = False

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant" and not st.session_state.first_interaction:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Send the welcome message
if st.session_state.first_interaction and not st.session_state.welcome_displayed:
    welcome_message = "Hello! Welcome to Gemini Chatbot! How may I help you today?"
    
    st.markdown(f'<div class="assistant-message">{welcome_message}</div>', unsafe_allow_html=True)

    tts = gTTS(text=welcome_message, lang='en')
    file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    try:
        tts.save(file_path)
        st.audio(file_path, format="audio/mp3")
    except PermissionError:
        st.write("Permission denied: unable to save or access 'response.mp3'.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.first_interaction = False
    st.session_state.welcome_displayed = True

# Voice input button
audio_data = audio_recorder()

if audio_data:
    st.write("Processing audio...")
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.write(audio_data)
    audio_file.flush()

    # Set up Google Cloud Speech-to-Text client
    client = speech.SpeechClient()
    with open(audio_file.name, "rb") as audio:
        content = audio.read()
    
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    audio_content = speech.RecognitionAudio(content=content)
    response = client.recognize(config=audio_config, audio=audio_content)

    if response.results:
        user_prompt = response.results[0].alternatives[0].transcript
        st.write(f"You said: {user_prompt}")
        
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.markdown(f'<div class="user-message">{user_prompt}</div>', unsafe_allow_html=True)

        gemini_answer = st.session_state.chat_session.send_message(user_prompt)
        st.session_state.messages.append({"role": "assistant", "content": gemini_answer.text})
        st.markdown(f'<div class="assistant-message">{gemini_answer.text}</div>', unsafe_allow_html=True)

        tts = gTTS(text=gemini_answer.text, lang='en')
        file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        try:
            tts.save(file_path)
            st.audio(file_path, format="audio/mp3")
        except PermissionError:
            st.write("Permission denied: unable to save or access 'response.mp3'.")
        except Exception as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("No speech detected.")
