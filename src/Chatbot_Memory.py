#working code for GroQ API based Chatbot with memory
import os
import json
import streamlit as st
from groq import Groq  # import Groq class from groq library

# Correct Streamlit page configuration
st.set_page_config(
    page_title='Llama3.1 Chat New', #tab name with icon
    page_icon='🦙'  # tab icon, get it from Emoji icon web page
)

# Setup config file
#config_file_path = r'C:\Users\Admin\Downloads\GroQ_Streamlit_Chatbot\src\config.json'
#working_dir = os.path.dirname(os.path.abspath(__file__))  # getting the current dir using code
config_file_path = 'Sample_Chatbot/src/config.json'
# Load config data
#config_data = json.load(open(config_file_path))
try:
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    st.error(f"Config file not found at {config_file_path}")
    raise
except json.JSONDecodeError:
    st.error(f"Error decoding JSON from config file at {config_file_path}")
    raise

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Save the API key to the environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize the chat history as Streamlit session if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # initially no history so []

# Streamlit page title
st.title('🦙 Llama3.1 Chatbot')  # application name

# Display chat history
for message in st.session_state.chat_history:  # iterate over every message in history and display
    with st.chat_message(message['role']):  # display content with every role, both user and LLM
        st.markdown(message['content'])

# Input field for user message or prompt
user_prompt = st.chat_input('Ask LLAMA...')  # accepts user prompt

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})  # appending user query

    # Send user message to LLM and get response
    messages = [
        {'role': 'system', 'content': 'content is helpful'},
        *st.session_state.chat_history
    ]
    response = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=messages
    )

    # Corrected access to message content
    assistant_response = response.choices[0].message.content  # Accessing content correctly
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})  # appending LLM response

    # Display LLM response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
