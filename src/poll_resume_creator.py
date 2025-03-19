"""Entry point for the application."""

import datetime
import os

from dotenv import load_dotenv

from aws.sqs import delete_message, fetch_messages
from handlers.process_resume_creator import local_invoke as resume_invoke
from utils.logger import logger

load_dotenv(dotenv_path=".env", override=True)


def main():
    """Entry point for the application."""
    resume_creation_queue_url = os.getenv("RESUME_CREATOR_QUEUE_URL")
    while True:
        logger.info(f"Current Time: {datetime.datetime.now()}")
        messages = fetch_messages(resume_creation_queue_url)
        try:
            for message in messages:
                if message:
                    message_body = message.get("Body")
                    resume_invoke(message_body)
                    delete_message(
                        queue_url=resume_creation_queue_url,
                        receipt_handle=message.get("ReceiptHandle"),
                    )
        except Exception as e:
            logger.error(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
