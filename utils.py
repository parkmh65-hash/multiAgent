import os
import json

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from models import Task


BASE_DIR = "data"


def get_user_path(thread_id):

    path = os.path.join(
        BASE_DIR,
        thread_id
    )

    os.makedirs(
        path,
        exist_ok=True
    )

    return path



def save_state(thread_id, state):

    path = get_user_path(thread_id)

    data = {

        "messages": [
            {
                "type": m.__class__.__name__,
                "content": m.content
            }
            for m in state["messages"]
        ],

        "task_history": [
            t.to_dict()
            for t in state.get(
                "task_history",
                []
            )
        ]
    }


    with open(
        f"{path}/state.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )



def load_state(thread_id):

    path = get_user_path(thread_id)

    file = f"{path}/state.json"


    if not os.path.exists(file):
        return None


    with open(
        file,
        encoding="utf-8"
    ) as f:

        data=json.load(f)


    messages=[]


    for m in data["messages"]:

        cls=m["type"]

        if cls=="HumanMessage":
            messages.append(
                HumanMessage(
                    content=m["content"]
                )
            )

        elif cls=="AIMessage":
            messages.append(
                AIMessage(
                    content=m["content"]
                )
            )

        elif cls=="SystemMessage":
            messages.append(
                SystemMessage(
                    content=m["content"]
                )
            )


    tasks=[
        Task(**x)
        for x in data.get(
            "task_history",
            []
        )
    ]


    return {

        "messages": messages,

        "task_history": tasks,

        "thread_id": thread_id
    }



def get_outline(thread_id):

    path=get_user_path(thread_id)

    file=f"{path}/outline.md"


    if not os.path.exists(file):

        return "아직 작성된 목차가 없습니다."


    with open(
        file,
        encoding="utf-8"
    ) as f:

        return f.read()



def save_outline(
    thread_id,
    outline
):

    path=get_user_path(thread_id)


    with open(
        f"{path}/outline.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(outline)
