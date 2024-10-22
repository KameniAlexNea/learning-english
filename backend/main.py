import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"],)
model_name = "gpt-4o-mini"

# Replace with your OpenAI API key
# openai.api_key = "YOUR_OPENAI_API_KEY"


class UserInput(BaseModel):
    user_input: str
    topic: str

SYSTEM_PROMPT = """
You are an AI assistant tasked with suggesting a writing topic and providing a brief commentary to help someone improve their writing skills. 
Your goal is to provide an engaging and appropriate topic based on the user's writing level, along with a helpful commentary to guide their writing practice.

Generate a topic suggestion that is suitable for the user's. The topic should be specific enough to provide direction but open-ended enough to allow for creativity and exploration.

Next, create a brief commentary about the suggested topic. This commentary should:
1. Explain why the topic is suitable for the user's writing
2. Highlight potential areas of focus or exploration within the topic
3. Suggest one or two writing techniques or skills the user could practice while working on this topic

Please, use less than 200 words !!!
"""

def generate_prompt():
    try:
        print("Starting")
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
        raise HTTPException(status_code=500, detail=str(e))


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
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=350,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suggest_topic")
def suggest_topic():
    topic = generate_prompt()
    return {"topic": topic}


@app.post("/evaluate")
def evaluate(user_input: UserInput):
    evaluation = evaluate_response(user_input.user_input, user_input.topic)
    return {"evaluation": evaluation}

@app.post("/suggest_answer")
def suggest_answer(user_input: UserInput):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "assistant", "content": user_input.topic},
                {"role": "system", "content": "Generate a suggested answer for the following topic."},
                {"role": "user", "content": user_input.topic}
            ],
            max_tokens=350,
        )
        return {"suggested_answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
