"""Langchain utilties."""

from langchain_anthropic import ChatAnthropic
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


def call_structured_groq_api(
    model="llama-3.1-8b-instant",
    max_tokens=500,
    temperature=0.2,
    messages=[],
    schema=None,
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
    llm_groq = llm_groq.with_structured_output(schema, method="json_mode", strict=True)

    completion = llm_groq.invoke(messages)

    return completion


def call_anthropic_api(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    temperature=0.2,
    messages=[],
):
    """Make a call to Anthropic API using langchain's interface.

    Args:
        model (str): The model to use for generation
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in the response
        messages (list): List of messages to send to Anthropic

    Returns:
        str: The generated content from Anthropic
    """
    llm_anthropic = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
    )

    completion = llm_anthropic.invoke(messages)

    return completion.content


def call_structured_anthropic_api(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    temperature=0.2,
    messages=[],
    schema=None,
):
    """Make a call to Anthropic API using langchain's interface with structured output.

    Args:
        model (str): The model to use for generation
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in the response
        messages (list): List of messages to send to Anthropic
        schema: The schema to structure the output

    Returns:
        The structured output from Anthropic
    """
    llm_anthropic = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
    )
    llm_anthropic = llm_anthropic.with_structured_output(schema, method="json_mode", strict=True)

    completion = llm_anthropic.invoke(messages)

    return completion
