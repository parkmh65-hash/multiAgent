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



# =========================
# State 저장
# =========================

def save_state(
    thread_id,
    state
):

    path = get_user_path(
        thread_id
    )


    state_dict = {}


    # messages

    state_dict["messages"] = [

        (
            m.__class__.__name__,
            m.content
        )

        for m in state["messages"]

    ]



    # task history

    state_dict["task_history"] = [

        task.to_dict()

        for task in state.get(
            "task_history",
            []
        )

    ]



    # references

    references = state.get(
        "references",
        {
            "queries": [],
            "docs": []
        }
    )


    state_dict["references"] = {


        "queries":
            references.get(
                "queries",
                []
            ),


        "docs":
        [

            doc.metadata

            for doc in references.get(
                "docs",
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

            state_dict,

            f,

            indent=4,

            ensure_ascii=False

        )





# =========================
# State 불러오기
# =========================

def load_state(
    thread_id
):

    path = get_user_path(
        thread_id
    )


    file = f"{path}/state.json"


    if not os.path.exists(file):

        return None



    with open(
        file,
        encoding="utf-8"
    ) as f:

        data = json.load(f)



    messages=[]


    for msg in data["messages"]:

        role = msg[0]

        content = msg[1]


        if role=="HumanMessage":

            messages.append(
                HumanMessage(
                    content=content
                )
            )


        elif role=="AIMessage":

            messages.append(
                AIMessage(
                    content=content
                )
            )


        elif role=="SystemMessage":

            messages.append(
                SystemMessage(
                    content=content
                )
            )



    tasks=[

        Task(**task)

        for task in data.get(
            "task_history",
            []
        )

    ]



    return {

        "messages":
            messages,


        "task_history":
            tasks,


        "references":
        {

            "queries":
            data.get(
                "references",
                {}
            ).get(
                "queries",
                []
            ),


            "docs":
            []

        },


        "thread_id":
            thread_id

    }





# =========================
# Outline
# =========================

def get_outline(
    thread_id
):

    path = get_user_path(
        thread_id
    )


    file = f"{path}/outline.md"



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

    path = get_user_path(
        thread_id
    )


    with open(

        f"{path}/outline.md",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            outline
        )


    return outline
