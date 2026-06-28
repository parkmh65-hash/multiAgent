# agents.py

from google import genai
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


class ChatAgent:
    """Gemini와 대화하는 기본 에이전트"""

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def run(self, question: str) -> str:
        response = client.models.generate_content(
            model=self.model,
            contents=question
        )

        return response.text


class SummaryAgent:
    """긴 문서를 요약하는 에이전트"""

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def run(self, text: str) -> str:

        prompt = f"""
다음 내용을 핵심만 요약하세요.

{text}
"""

        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text


class TranslateAgent:
    """번역 에이전트"""

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def run(self, text: str, language="영어") -> str:

        prompt = f"""
다음 문장을 {language}로 번역하세요.

{text}
"""

        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text


class CodingAgent:
    """코드 생성 에이전트"""

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def run(self, request: str) -> str:

        prompt = f"""
당신은 Python 전문가입니다.

{request}
"""

        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text
