import streamlit as st

from learning_language.backend import (
    evaluate,
    prepare,
    suggest_llm_answer,
    suggest_topic,
)

st.title("Writing Assistant")

if "topic" not in st.session_state:
    st.session_state.topic = ""

if st.button("Generate New Topic"):
    response = suggest_topic()
    if "Error" not in response["topic"]:
        st.session_state.topic = response["topic"]
        st.success(response["topic"])
    else:
        st.error(response["topic"])

if st.session_state.topic:
    st.subheader("Current Topic")
    st.write(st.session_state.topic)

    user_input = st.text_area("Write your response here:")

    if st.button("Evaluate Response"):
        if user_input.strip():
            user_data = prepare(
                {"user_input": user_input, "topic": st.session_state.topic}
            )
            evaluation = evaluate(user_data)
            if "Error" not in evaluation["evaluation"]:
                st.success(evaluation["evaluation"])
            else:
                st.error(evaluation["evaluation"])
        else:
            st.warning("Please provide a response.")

    if st.button("Suggest an Answer"):
        user_data = prepare({"user_input": "", "topic": st.session_state.topic})
        suggested_answer = suggest_llm_answer(user_data)
        if "Error" not in suggested_answer["suggested_answer"]:
            st.success(suggested_answer["suggested_answer"])
        else:
            st.error(suggested_answer["suggested_answer"])
