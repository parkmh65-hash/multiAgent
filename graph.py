from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.messages import (
    SystemMessage,
    AIMessage,
)

from langchain_core.output_parsers import StrOutputParser

from utils import (
    get_outline,
    save_outline,
)

llm = ChatOpenAI(
    model="gpt-4o"
)
