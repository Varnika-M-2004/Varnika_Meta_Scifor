import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Set paths explicitly
ffmpeg_path = r"C:/Users/Varnika Mulay/Downloads/ffmpeg/bin/ffmpeg.exe"
ffprobe_path = r"C:/Users/Varnika Mulay/Downloads/ffmpeg/bin/ffprobe.exe"

# Set paths directly in pydub
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

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
    file_path = "response.mp3"
    try:
        tts.save(file_path)
        audio = AudioSegment.from_mp3(file_path)
        play(audio)
    except PermissionError:
        st.write("Permission denied: unable to save or access 'response.mp3'.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
    
    # Append the welcome message after playing it
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.first_interaction = False
    st.session_state.welcome_displayed = True

# Voice input button
if st.button("Talk to Gemini"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio_data = r.listen(source)
        try:
            # Recognize speech using Google Speech Recognition
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
            file_path = "response.mp3"
            try:
                tts.save(file_path)
                audio = AudioSegment.from_mp3(file_path)
                play(audio)
            except PermissionError:
                st.write("Permission denied: unable to save or access 'response.mp3'.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
        except sr.RequestError:
            st.write("Sorry, the service is unavailable at the moment.")
