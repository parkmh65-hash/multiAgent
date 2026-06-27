from typing import TypedDict, List

from langchain_core.messages import AnyMessage

from models import Task


class State(TypedDict):

    messages: List[AnyMessage]

    task_history: List[Task]

    thread_id: str
