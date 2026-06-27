from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

from utils import (
    get_outline,
    save_outline,
)

llm = ChatOpenAI(
    model="gpt-4o"
)


def content_strategist(state):
    """사용자 요구를 분석하여 책의 상세 목차를 작성한다."""

    print("CONTENT STRATEGIST")

    thread_id = state["thread_id"]
    outline = get_outline(thread_id)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
너는 책 집필 AI팀의 콘텐츠 전략가이다.

사용자의 요구를 분석하여
책의 상세 목차를 작성한다.

기존 목차:
{outline}
                """,
            ),
            MessagesPlaceholder("messages"),
        ]
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke(
        {
            "messages": state["messages"]
        }
    )

    save_outline(
        thread_id,
        result
    )

    return {
        "messages": [
            AIMessage(
                content="[Content Strategist] 목차 작성 완료"
            )
        ]
    }


def communicator(state):
    """현재 진행 상황을 사용자에게 설명하고 다음 작업을 안내한다."""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
너는 책 작성팀의 커뮤니케이터이다.

사용자에게 현재 진행 상황을 설명하고,
다음 작업을 위해 필요한 질문을 자연스럽게 이어간다.
                """,
            ),
            MessagesPlaceholder("messages"),
        ]
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": [
            result
        ]
    }
