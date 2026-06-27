from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime

from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from graph import graph

from utils import (
    load_state,
    save_state
)



app=FastAPI()



class ChatRequest(BaseModel):

    user_input:str

    thread_id:str="default"





@app.get("/")
def home():

    return {
        "status":"running"
    }




@app.post("/chat")
def chat(req:ChatRequest):


    state=load_state(
        req.thread_id
    )


    if state is None:

        state={

            "messages":[
                SystemMessage(
                    f"""
AI 책 집필팀입니다.

시간:
{datetime.now()}
"""
                )
            ],

            "task_history":[],

            "references":{
                "queries":[],
                "docs":[]
            },

            "thread_id":
                req.thread_id
        }




    state["messages"].append(
        HumanMessage(
            req.user_input
        )
    )


    result=graph.invoke(
        state
    )


    save_state(
        req.thread_id,
        result
    )


    return {

        "response":
        result["messages"][-1].content

    }
