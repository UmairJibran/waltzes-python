"""Handler for scraping job postings."""

from typing import Any, Dict

from handlers.base_handler import BaseHandler
from services.llm.json_schemas import JobStructure
from services.llm.langchain import call_structured_groq_api
from services.llm.prompts import system_prompt_job_stucturizor
from utils import logger
from utils.utils import add_query_param, send_data_to_callback_url


class JobStructureHandler(BaseHandler):
    """Handler for job scraping requests."""

    def process_message(self, message_body: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single job scraping message.

        Args:
            message_body (Dict[str, Any]): The parsed message body containing the job URL

        Returns:
            Dict[str, Any]: Response containing the scraped job details
        """
        # logger.info(f"Processing job scraping request: {message_body}")

        job_url = message_body.get("jobUrl")
        selected_text = message_body.get("selectedText")
        callback_url = message_body.get("callbackUrl")
        logger.info(f"""{callback_url=}""")
        if not job_url:
            raise ValueError("Job Url is required")
        if not selected_text:
            raise ValueError("Selected Text is required")
        start_notification_url = add_query_param(callback_url, "just-started", "true")
        send_data_to_callback_url({}, start_notification_url)
        response = call_structured_groq_api(
            model="llama3-8b-8192",
            max_tokens=8192,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt_job_stucturizor,
                },
                {"role": "user", "content": selected_text},
            ],
            schema=JobStructure,
        )
        logger.critical(f"""{response=}""")
        send_data_to_callback_url(response, callback_url)


handler_instance = JobStructureHandler()
handler = handler_instance.handler
local_invoke = handler_instance.local_invoke
