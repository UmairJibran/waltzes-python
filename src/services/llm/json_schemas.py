"""JSON Schemas for LLMs."""

from typing import Annotated, TypedDict


# PyDantic
class JobStructure(TypedDict):
    """JOB Schema."""

    title: Annotated[str, ..., "The title of the job"]
    description: Annotated[str, ..., "The description of the job"]
    companyName: Annotated[str, ..., "The name of the company"]
    skills: Annotated[list[str], ..., "The skills required for the job"]
    location: Annotated[str, ..., "The location of the job"]
    jobType: Annotated[str, ..., "The type of job"]
    salary: Annotated[str, ..., "The salary range"]
