import json
import logging
import os

__author__ = 'sanketh'
__email__ = 'sanketh@github'
__version__ = '0.0.1'
__status__ = 'production'


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "konstone_hello_world"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())

    LOGGER.info(f"received_event:{event}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Hello from {global_args.OWNER} {context.function_name}! You invoked Lambda through API GW"
        })
    }