from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import State

from agents import (
    supervisor,
    supervisor_router,
    content_strategist,
    communicator
)


builder=StateGraph(State)


builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "content_strategist",
    content_strategist
)

builder.add_node(
    "communicator",
    communicator
)



builder.add_edge(
    START,
    "supervisor"
)


builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "content_strategist":
            "content_strategist",

        "communicator":
            "communicator"
    }
)


builder.add_edge(
    "content_strategist",
    "communicator"
)


builder.add_edge(
    "communicator",
    END
)



graph=builder.compile()
