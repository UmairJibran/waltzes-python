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


class ResumeStructure(TypedDict):
    """RESUME Schema."""

    name: Annotated[str, ..., "The name of the applicant"]
    summary: Annotated[str, ..., "The summary of the applicant"]
    location: Annotated[str, ..., "The location of the applicant"]
    skills: Annotated[list[str], ..., "The skills of the applicant"]
    contact: Annotated[list[str], ..., "The contact information of the applicant, including email, phone, linkedin, github, and portfolio etc"]
    experience: Annotated[list[dict], ..., "The experience of the applicant"]
    education: Annotated[list[dict], ..., "The education of the applicant"]
    certifications: Annotated[list[str], ..., "The certifications of the applicant"]
    open_source: Annotated[list[str], ..., "The open source contributions of the applicant"]
    projects: Annotated[list[str], ..., "The projects of the applicant"]