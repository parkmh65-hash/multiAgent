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
    communicator,
    vector_search_agent
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


builder.add_node(
    "vector_search_agent",
    vector_search_agent
)



builder.add_edge(
    START,
    "supervisor"
)



builder.add_conditional_edges(
    "supervisor",
    supervisor_router
)



builder.add_edge(
    "content_strategist",
    "communicator"
)


builder.add_edge(
    "vector_search_agent",
    "communicator"
)



builder.add_edge(
    "communicator",
    END
)



graph=builder.compile()
