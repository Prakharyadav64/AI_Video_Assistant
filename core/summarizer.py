
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_llm():
    return ChatOllama(
        model="qwen2.5:3b",
        temperature=0.3
    )


def generate_title(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "Untitled"

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Generate a short, accurate title for the actual content. "
            "Do not assume it is a meeting. Return only the title."
        ),
        ("human", "{text}")
    ])

    chain = prompt | get_llm() | StrOutputParser()
    return chain.invoke({"text": transcript}).strip()


def summarize(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No transcript available to summarize."

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Summarize the actual content of the provided text in "
            "concise bullet points. Do not assume the content is a "
            "meeting, conversation, or lecture. Never write phrases "
            "such as 'The meeting discussed' unless the transcript "
            "explicitly establishes that it is a meeting. Do not "
            "invent facts or add unsupported information. Preserve "
            "important names, dates, numbers, and key ideas. Use "
            "4-6 bullet points for long text and fewer for short text."
        ),
        ("human", "{text}")
    ])

    chain = prompt | get_llm() | StrOutputParser()
    return chain.invoke({"text": transcript}).strip()