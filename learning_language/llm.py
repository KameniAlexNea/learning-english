import os

import ollama
import openai

from .model_dataclass import *
from .prompts import *

OLLAMA_CONFIG = {"model": os.environ.get("OLLAMA_CONFIG_MODEL", None)}

OPENAI_CONFIG = {
    "model": os.environ.get("OLLAMA_CONFIG_MODEL", None),
    "api_key": os.environ.get("OPENAI_API_KEY", None),
}

client = (
    openai.OpenAI(
        api_key=OPENAI_CONFIG["api_key"],
    )
    if OPENAI_CONFIG["api_key"] is not None
    else None
)


def ollama_chat(messages):
    try:
        response = ollama.chat(
            model=OLLAMA_CONFIG["model"],
            messages=messages,
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error generating prompt: {str(e)}"


def openai_chat(
    messages,
):
    try:
        response = client.chat.completions.create(
            model=OPENAI_CONFIG["model"],
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating prompt: {str(e)}"


chat_function = openai_chat if os.environ["USE_OPENAI"] == "1" else ollama_chat


def generate_prompt():
    return chat_function(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
        ]
    )


def evaluate_response(user_input: str, topic: str):
    messages = [
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
            "content": f"Evaluate the following response for clarity, grammar, and provide suggestions. Discuss also the user ability to follow the subject. Your evaluation should be written in " + LANGUAGE,
        },
        {"role": "user", "content": user_input},
    ]
    return chat_function(messages)


def suggest_answer(user_input: UserInput):
    messages = [
        {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_input.topic},
        {
            "role": "system",
            "content": ANSWER_PROMPT,
        },
    ]
    return chat_function(messages)
