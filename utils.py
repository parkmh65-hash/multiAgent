import os
import json

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from models import Task


BASE_DIR="data"



def get_user_path(thread_id):

    path=os.path.join(
        BASE_DIR,
        thread_id
    )

    os.makedirs(
        path,
        exist_ok=True
    )

    return path



def save_state(thread_id,state):

    path=get_user_path(
        thread_id
    )


    data={}


    data["messages"]=[

        {
            "type":m.__class__.__name__,
            "content":m.content
        }

        for m in state["messages"]

    ]



    data["task_history"]=[

        t.to_dict()

        for t in state.get(
            "task_history",
            []
        )

    ]



    refs=state.get(
        "references",
        {
            "queries":[],
            "docs":[]
        }
    )


    data["references"]={

        "queries":
            refs.get("queries",[]),

        "docs":
        [
            d.metadata
            for d in refs.get("docs",[])
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
            indent=4,
            ensure_ascii=False
        )





def load_state(thread_id):

    path=get_user_path(
        thread_id
    )

    file=f"{path}/state.json"


    if not os.path.exists(file):

        return None



    with open(
        file,
        encoding="utf-8"
    ) as f:

        data=json.load(f)



    messages=[]


    for m in data["messages"]:

        if m["type"]=="HumanMessage":

            messages.append(
                HumanMessage(
                    m["content"]
                )
            )


        elif m["type"]=="AIMessage":

            messages.append(
                AIMessage(
                    m["content"]
                )
            )


        else:

            messages.append(
                SystemMessage(
                    m["content"]
                )
            )



    return {

        "messages":messages,

        "task_history":
        [
            Task(**x)
            for x in data["task_history"]
        ],

        "references":
        {
            "queries":
            data["references"]["queries"],

            "docs":[]
        },

        "thread_id":thread_id
    }





def get_outline(thread_id):

    path=get_user_path(
        thread_id
    )


    file=f"{path}/outline.md"


    if not os.path.exists(file):

        return "아직 작성된 목차가 없습니다."



    return open(
        file,
        encoding="utf-8"
    ).read()




def save_outline(thread_id,text):

    path=get_user_path(
        thread_id
    )


    with open(
        f"{path}/outline.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)


    return text
