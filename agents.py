from datetime import datetime

from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    AIMessage
)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import (
    get_outline,
    save_outline
)

from models import Task


llm = ChatOpenAI(
    model="gpt-4o"
)



def supervisor(state):

    prompt = PromptTemplate.from_template(
"""
너는 AI 팀 supervisor이다.

가능한 agent:
- content_strategist
- communicator

현재 해야 할 agent만 반환한다.

목차:
{outline}

대화:
{messages}
"""
    )


    chain = (
        prompt
        | llm.with_structured_output(Task)
    )


    task = chain.invoke(
        {
            "outline":
                get_outline(
                    state["thread_id"]
                ),

            "messages":
                state["messages"]
        }
    )


    history = state.get(
        "task_history",
        []
    )

    history.append(task)


    return {

        "messages":[
            AIMessage(
                content=f"[Supervisor] {task.agent}"
            )
        ],

        "task_history": history
    }



def supervisor_router(state):

    return (
        state["task_history"][-1]
        .agent
    )



def content_strategist(state):

    prompt = PromptTemplate.from_template(
"""
너는 콘텐츠 전략가이다.

목차를 작성한다.

기존:
{outline}

대화:
{messages}
"""
    )


    chain = (
        prompt
        | llm
        | StrOutputParser()
    )


    result = chain.invoke(
        {
            "outline":
            get_outline(
                state["thread_id"]
            ),

            "messages":
            state["messages"]
        }
    )


    save_outline(
        state["thread_id"],
        result
    )


    history=state["task_history"]

    history[-1].done=True
    history[-1].done_at=datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    return {

        "messages":[
            AIMessage(
                content=
                "[Content Strategist] 목차 작성 완료"
            )
        ],

        "task_history":history
    }




def communicator(state):

    prompt = PromptTemplate.from_template(
"""
너는 communicator이다.

사용자에게 진행상황을 설명한다.

대화:
{messages}
"""
    )


    result = (
        prompt | llm
    ).invoke(
        {
            "messages":
            state["messages"]
        }
    )


    history=state["task_history"]

    history[-1].done=True
    history[-1].done_at=datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    return {

        "messages":[result],

        "task_history":history
    }
