import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Updated to match FastAPI's default port


def get_topic():
    response = requests.get(f"{API_URL}/suggest_topic")
    if response.status_code == 200:
        return response.json().get("topic")
    return "Error fetching topic."


def evaluate_input(user_input):
    response = requests.post(f"{API_URL}/evaluate", json={"user_input": user_input, 'topic': st.session_state["topic"]})
    if response.status_code == 200:
        return response.json().get("evaluation")
    return "Error evaluating input."

def suggest_answer():
    response = requests.post(f"{API_URL}/suggest_answer", json={"topic": st.session_state["topic"], "user_input": ""})
    if response.status_code == 200:
        return response.json().get("suggested_answer")
    return "Error generating a suggested answer."


st.title("English Learning Tool")

if "topic" not in st.session_state:
    st.session_state["topic"] = get_topic()

st.write(f"**Suggested Topic:** {st.session_state['topic']}")

user_input = st.text_area("Your response:", height=200)

if st.button("Evaluate"):
    if user_input:
        evaluation = evaluate_input(user_input)
        st.write(f"**Feedback:**\n{evaluation}")
    else:
        st.write("Please enter a response.")

if st.button("Suggest New Topic"):
    st.rerun()
    # st.session_state["topic"] = get_topic()
    # st.write(f"**Suggested Topic:** {st.session_state['topic']}")


if st.button("Suggest an Answer"):
    suggested_answer = suggest_answer()
    st.write(f"**Suggested Answer:**\n{suggested_answer}")