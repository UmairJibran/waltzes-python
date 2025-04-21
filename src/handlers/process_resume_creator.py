"""Handler for creating resumes."""

import json
import time
from typing import Any, Dict

from services.llm.json_schemas import ResumeStructure
from handlers.base_handler import BaseHandler
from services.llm.langchain import call_structured_groq_api, call_openai_api
from services.llm.prompts import (
    system_prompt_resume_segmentation,
    user_prompt_for_resume_creation,
)
from utils import logger
from utils.utils import (
    add_query_param,
    parse_json_from_llm,
    send_data_to_callback_url,
)


def clean_title(text: str) -> str:
    """Clean the title for use in filenames."""
    return (
        text.replace(",", "")
        .replace("&", "and")
        .replace("(", "")
        .replace(")", "")
        .replace("-", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace(" ", "_")
        .lower()
    )


class ResumeCreatorHandler(BaseHandler):
    """Handler for resume creation requests."""

    def process_message(self, message_body: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single resume creation message.

        Args:
            message_body (Dict[str, Any]): The parsed message body containing job and applicant details

        Returns:
            Dict[str, Any]: Response containing the generated resume file path
        """
        logger.info(f"Processing resume creation request: {message_body}")

        job_details = message_body.get("jobDetails", {})
        applicant_details = message_body.get("applicantDetails", {})
        llm_model = message_body.get("llmModel", "groq")

        callback_url = message_body.get("callbackUrl")
        linkedin_data = applicant_details.get("linkedinScrapedData")
        job_skills_listed = job_details.get("skills")
        applicant_email = applicant_details.get("email")
        applicant_phone = applicant_details.get("phone")
        applicant_portfolio = applicant_details.get("portfolioUrl")
        applicant_github = applicant_details.get("githubUsername")
        applicant_linkedin = applicant_details.get("linkedinUsername")
        applicant_first_name = applicant_details.get("firstName")
        applicant_last_name = applicant_details.get("lastName")
        applicant_additional_instructions = applicant_details.get(
            "additionalInstructions"
        )

        start_notification_url = add_query_param(
            callback_url, "just-started", "true")
        send_data_to_callback_url({}, start_notification_url)
        # log all the details
        logger.info(f"Applicant Details: {applicant_details}")
        logger.info(f"Job Details: {job_details}")
        logger.info(f"Callback URL: {callback_url}")
        logger.info(f"Linkedin Data: {linkedin_data}")
        logger.info(f"Job Skills: {job_skills_listed}")
        logger.info(f"Applicant Email: {applicant_email}")
        logger.info(f"Applicant Phone: {applicant_phone}")
        logger.info(f"Applicant Portfolio: {applicant_portfolio}")
        logger.info(f"Applicant Github: {applicant_github}")
        logger.info(f"Applicant LinkedIn: {applicant_linkedin}")
        logger.info(f"Applicant First Name: {applicant_first_name}")
        logger.info(f"Applicant Last Name: {applicant_last_name}")
        logger.info(
            f"Applicant Additional Instructions: {applicant_additional_instructions}"
        )

        # parse user prompt
        user_prompt = user_prompt_for_resume_creation.format(
            user_linkedin_data=linkedin_data,
            job_details=job_details,
            additional_info=json.dumps(
                {
                    "email": applicant_email,
                    "phone": applicant_phone,
                    "portfolio": applicant_portfolio,
                    "github": applicant_github,
                    "linkedin": applicant_linkedin,
                    "firstName": applicant_first_name,
                    "lastName": applicant_last_name,
                    "additionalInstructions": applicant_additional_instructions,
                }
            ),
        )
        logger.info(f"""{user_prompt=}""")

        start_time = time.time()

        match llm_model:
            case "groq":
                logger.info("Using GROQ model for resume creation")
                resume_segments = call_structured_groq_api(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    max_tokens=8192,
                    temperature=0.4,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt_resume_segmentation,
                        },
                        {"role": "user", "content": user_prompt},
                    ],
                    schema=ResumeStructure,
                )
            case "openai":
                logger.info("Using OpenAI model for resume creation")
                resume_segments = call_openai_api(
                    model="gpt-4o",
                    max_tokens=5000,
                    temperature=0.3,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt_resume_segmentation,
                        },
                        {"role": "user", "content": user_prompt},
                    ],
                )

        print(f"Time taken: {time.time() - start_time}")

        logger.critical(f"""{resume_segments=}""")
        send_data_to_callback_url(
            data=resume_segments, callback_url=callback_url)


# Create a singleton instance
handler_instance = ResumeCreatorHandler()
handler = handler_instance.handler
local_invoke = handler_instance.local_invoke
