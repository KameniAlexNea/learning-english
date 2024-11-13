from pydantic import BaseModel


class UserInput(BaseModel):
    user_input: str
    topic: str


def prepare(obj: dict):
    return UserInput(**obj)
