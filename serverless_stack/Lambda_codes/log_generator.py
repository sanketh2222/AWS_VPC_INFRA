import json
import os
import random
from time import sleep
import logging


    
def random_generator():
    n=os.getenv('Percentage_error',80)# get the value from env varable, 80 is default value if env vvar value is not available
    ind=False
    if random.randint(1, 100) < int(n):
        sleep(1)
        ind=True
        
    return ind
    
def third_party_api_call():
    resp=random_generator()
    return resp
    
def lambda_handler(event, context):
    # TODO implement
    # error =os.getenv('Percentage_error',80)
    # ex_time=context.get_remaining_time_in_millis()
    # print("time is ",ex_time)
    # print('error is',error)
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())
    
    LOGGER.info(f"event is {event}")
    
    fmt_log_msg = {
        "third_party_api_error": False
    }
    
    api_call=third_party_api_call()
    
    if api_call:
        fmt_log_msg["third_party_api_error"]=True
        fmt_log_msg["remaining_time_in_millis"] = context.get_remaining_time_in_millis()
        
    det=json.dumps(fmt_log_msg)
    
    LOGGER.info(det)
    
    return {
        'statusCode': 200,
        'body': det
    }
# import os
# print(os.getcwd())