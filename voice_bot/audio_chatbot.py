import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Set up paths for ffmpeg and ffprobe
AudioSegment.converter = "C:/Users/Varnika Mulay/Downloads/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffmpeg = "C:/Users/Varnika Mulay/Downloads/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = "C:/Users/Varnika Mulay/Downloads/ffmpeg/bin/ffprobe.exe"

# Initialize sounddevice for audio input/output
def record_audio(duration=5, samplerate=44100):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()
    return audio_data, samplerate

def save_audio_to_temp_file(audio_data, samplerate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, samplerate, audio_data)
        return tmpfile.name

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
GOOGLE_API_KEY = st.secrets["google"]["api_key"]

# Set up and define the Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

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

    # Play the welcome message
    tts = gTTS(text=welcome_message, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        audio = AudioSegment.from_mp3(tmpfile.name)
        play(audio)

    # Append the welcome message after playing it
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.first_interaction = False
    st.session_state.welcome_displayed = True

# Voice input button
if st.button("Talk to Gemini"):
    audio_data, samplerate = record_audio()
    temp_audio_path = save_audio_to_temp_file(audio_data, samplerate)
    
    try:
        # Recognize speech using Google Speech Recognition
        r = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = r.record(source)
            user_prompt = r.recognize_google(audio_data)
        st.write(f"You said: {user_prompt}")
        
        # Add user's question to chat and display it
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.markdown(f'<div class="user-message">{user_prompt}</div>', unsafe_allow_html=True)

        # Send user's question to Gemini-Pro and get answer
        gemini_answer = st.session_state.chat_session.send_message(user_prompt)

        # Display and voice the answer
        st.session_state.messages.append({"role": "assistant", "content": gemini_answer.text})
        st.markdown(f'<div class="assistant-message">{gemini_answer.text}</div>', unsafe_allow_html=True)

        # Generate and play voice response for the latest message only
        tts = gTTS(text=gemini_answer.text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            audio = AudioSegment.from_mp3(tmpfile.name)
            play(audio)

    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
    except sr.RequestError:
        st.write("Sorry, the service is unavailable at the moment.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
