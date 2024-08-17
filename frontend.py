import streamlit as st

from backend import evaluate, prepare, suggest_topic, suggest_llm_answer


def get_topic():
    response = suggest_topic()
    return response.get("topic")


def evaluate_input(user_input):
    response = evaluate(prepare({"user_input": user_input, 'topic': st.session_state["topic"]}))
    return response.get("evaluation")

def suggest_answer():
    response = suggest_llm_answer(prepare({"topic": st.session_state["topic"], "user_input": ""}))
    return response.get("suggested_answer")


st.title("English Learning Tool")

if "topic" not in st.session_state:
    st.session_state["topic"] = get_topic()

st.write(f"**Suggested Topic:** \n{st.session_state['topic']}")

user_input = st.text_area("Your response:", height=200)

if st.button("Evaluate"):
    if user_input:
        evaluation = evaluate_input(user_input)
        st.write(f"**Feedback:**\n{evaluation}")
    else:
        st.write("Please enter a response.")

if st.button("Suggest New Topic"):
    st.session_state.clear()
    st.rerun()
    # st.session_state["topic"] = get_topic()
    # st.write(f"**Suggested Topic:** {st.session_state['topic']}")


if st.button("Suggest an Answer"):
    suggested_answer = suggest_answer()
    st.write(f"**Suggested Answer:**\n{suggested_answer}")