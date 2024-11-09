import streamlit as st
import requests

st.title("One-Day Tour Planner Chatbot")

if 'current_response' not in st.session_state:
    st.session_state['current_response'] = ""

if st.button("Start New Session"):
    requests.post("http://127.0.0.1:8000/start_session")
    st.session_state['current_response'] = ""
    st.success("New session started.")

user_input = st.text_input("You:")

if st.button("Send") and user_input:
    response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
    
    if response.status_code == 200:
        st.session_state['current_response'] = response.json().get("reply", "No response")
    else:
        st.session_state['current_response'] = "Error connecting to server"

st.write("Bot:", st.session_state['current_response'])




