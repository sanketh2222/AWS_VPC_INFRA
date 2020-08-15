import json
import logging
import os


def lambda_handler(event, context):
    global LOGGER_VAR
    LOGGER_VAR = logging.getLogger()
    LOGGER_VAR.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())

    LOGGER_VAR.info(f"received_event:{event}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": event
        })
    }