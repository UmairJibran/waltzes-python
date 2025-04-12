"""Entry point for the application."""

import datetime
import os

from dotenv import load_dotenv

from aws.sqs import delete_message, fetch_messages
from handlers.process_job_structuror import local_invoke as job_invoke
from utils.logger import logger

load_dotenv(dotenv_path=".env", override=True)


def main():
    """Entry point for the application."""
    structuror_queue_url = os.getenv("JOB_STRUCTUROR_QUEUE_URL")
    while True:
        logger.info(f"Current Time: {datetime.datetime.now()}")
        messages = fetch_messages(structuror_queue_url)
        try:
            for message in messages:
                if message:
                    message_body = message.get("Body")
                    job_invoke(message_body)
                    delete_message(
                        queue_url=structuror_queue_url,
                        receipt_handle=message.get("ReceiptHandle"),
                    )
        except Exception as e:
            logger.error(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
