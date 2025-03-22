"""Langchain utilties."""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def call_openai_api(
    model="gpt-4o",
    max_tokens=500,
    temperature=0.2,
    messages=[],
):
    """Make a call to OpenAI API using langchain's interface.

    Args:
        model (str): The model to use for generation
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in the response
        messages (list): List of messages to send to OpenAI

    Returns:
        str: The generated content from OpenAI
    """
    llm_openai = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
    )

    completion = llm_openai.invoke(messages)

    return completion.content


def call_groq_api(
    model="llama-3.3-70b-versatile",
    max_tokens=500,
    temperature=0.2,
    messages=[],
):
    """Make a call to Groq API using langchain's interface.

    Args:
        model (str): The model to use for generation
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in the response
        messages (list): List of messages to send to Groq

    Returns:
        str: The generated content from Groq
    """
    llm_groq = ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
    )

    completion = llm_groq.invoke(messages)

    return completion.content
