import os

import openai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)
model_name = "gpt-4o-mini"


SYSTEM_PROMPT = """
You are an AI assistant tasked with providing a writing topic and a brief, insightful commentary to help someone enhance their writing skills. Your goal is to offer an engaging and appropriate topic tailored to the user’s writing level. The topic should avoid clichés like "A day in the life of..." and steer clear of focusing on objects. Aim for a topic that is specific enough to give direction yet open-ended enough to encourage creativity and exploration.

After suggesting the topic, provide a brief commentary that:
1. Explains why the topic suits the user's writing level.
2. Identifies key areas for exploration within the topic.
3. Recommends one or two writing techniques or skills the user can practice while working on this topic.

Ensure the commentary is concise and stays under 200 words.
"""


class UserInput(BaseModel):
    user_input: str
    topic: str


def prepare(obj: dict):
    return UserInput(**obj)


def generate_prompt():
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                }
            ],
            max_tokens=250,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)  # fix this in request


def evaluate_response(user_input: str, topic: str):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "assistant",
                    "content": topic,
                },
                {
                    "role": "system",
                    "content": f"Evaluate the following response for clarity, grammar, and provide suggestions. Discuss also the user ability to follow the subject.",
                },
                {"role": "user", "content": user_input},
            ],
            max_tokens=350,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)  # fix this in request


def suggest_answer(user_input: UserInput):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "assistant", "content": user_input.topic},
                {
                    "role": "system",
                    "content": "Generate a suggested answer for the following topic.",
                },
                {"role": "user", "content": user_input.topic},
            ],
            max_tokens=350,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)  # fix this in request


def suggest_topic():
    return {"topic": generate_prompt()}


def evaluate(user_input: UserInput):
    evaluation = evaluate_response(user_input.user_input, user_input.topic)
    return {"evaluation": evaluation}


def suggest_llm_answer(user_input: UserInput):
    response = suggest_answer(user_input)
    return {"suggested_answer": response}
