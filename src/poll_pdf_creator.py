"""Entry point for the pdf processor."""

import datetime
import os

from dotenv import load_dotenv

from aws.sqs import delete_message, fetch_messages
from handlers.process_pdf_creator import local_invoke as pdf_invoke
from utils.logger import logger

load_dotenv(dotenv_path=".env", override=True)


def main():
    """Entry point for the pdf processor."""
    pdf_processor_queue_url = os.getenv("PDF_PROCESSOR_QUEUE_URL")
    while True:
        logger.info(f"Current Time: {datetime.datetime.now()}")
        messages = fetch_messages(pdf_processor_queue_url)
        try:
            for message in messages:
                if message:
                    message_body = message.get("Body")
                    pdf_invoke(message_body)
                    delete_message(
                        queue_url=pdf_processor_queue_url,
                        receipt_handle=message.get("ReceiptHandle"),
                    )
        except Exception as e:
            logger.error(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
