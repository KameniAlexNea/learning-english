from dotenv import load_dotenv

from .llm import *

load_dotenv()


def suggest_topic():
    return {"topic": generate_prompt()}


def evaluate(user_input: UserInput):
    evaluation = evaluate_response(user_input.user_input, user_input.topic)
    return {"evaluation": evaluation}


def suggest_llm_answer(user_input: UserInput):
    response = suggest_answer(user_input)
    return {"suggested_answer": response}
