
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def _get_llm():
    return ChatOllama(model="qwen2.5:3b", temperature=0)


def _ask_llm(text: str, instruction: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", instruction),
        ("human", "{text}")
    ])
    chain = prompt | _get_llm() | StrOutputParser()
    return chain.invoke({"text": text}).strip()


def extract_action_items(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No action items found."

    # Avoid calling an LLM for obviously unrelated content.
    pattern = re.compile(
        r"\b(?:will|must|should|need to|needs to|has to|have to|"
        r"assigned to|responsible for)\b",
        re.IGNORECASE
    )

    if not pattern.search(transcript):
        return "No action items found."

    instruction = (
        "Extract only explicit action items from the text. "
        "Include an owner and deadline only when explicitly stated. "
        "Do not invent tasks, owners, or deadlines. "
        "If none exist, return exactly: No action items found."
    )
    return _ask_llm(transcript, instruction)


def extract_key_decisions(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No key decisions found."

    pattern = re.compile(
        r"\b(?:decided|decision|agreed|approved|selected|chose|"
        r"will use|going with)\b",
        re.IGNORECASE
    )

    if not pattern.search(transcript):
        return "No key decisions found."

    instruction = (
        "Extract only decisions explicitly made in the text. "
        "Do not mistake general facts or historical events for decisions. "
        "Do not invent information. "
        "If none exist, return exactly: No key decisions found."
    )
    return _ask_llm(transcript, instruction)


def extract_questions(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No questions found."

    questions = re.findall(
        r"[^.!?\n]*\?",
        transcript
    )

    if not questions:
        return "No questions found."

    return "\n".join(
        f"{i}. {question.strip()}"
        for i, question in enumerate(questions, start=1)
    )
