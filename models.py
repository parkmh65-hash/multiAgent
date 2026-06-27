from pydantic import BaseModel, Field
from typing import Literal, Optional


class Task(BaseModel):

    agent: Literal[
        "content_strategist",
        "communicator",
    ] = Field(...)


    done: bool = False


    description: str


    done_at: Optional[str] = None


    def to_dict(self):

        return {
            "agent": self.agent,
            "done": self.done,
            "description": self.description,
            "done_at": self.done_at
        }
