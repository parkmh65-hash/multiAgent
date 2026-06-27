from pydantic import BaseModel, Field
from typing import Literal, Optional


class Task(BaseModel):

    agent: Literal[
        "content_strategist",
        "communicator",
        "vector_search_agent"
    ]


    done: bool = False


    description: str


    done_at: Optional[str] = None


    def to_dict(self):

        return self.model_dump()
