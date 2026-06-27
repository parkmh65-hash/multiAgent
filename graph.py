from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from state import State
from agents import (
    content_strategist,
    communicator,
)

builder = StateGraph(State)

builder.add_node(
    "strategist",
    content_strategist,
)

builder.add_node(
    "communicator",
    communicator,
)

builder.add_edge(
    START,
    "strategist",
)

builder.add_edge(
    "strategist",
    "communicator",
)

builder.add_edge(
    "communicator",
    END,
)

graph = builder.compile()
