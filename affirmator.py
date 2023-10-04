import os
from dotenv import load_dotenv
from twilio.rest import Client
import config
import random


def get_affirmations() -> list:
    """
    function to get an integer number of affirmations from the list in config

    :return: list of 3 affirmations randomly sampled from config list
    """ 
    if (len(config.AFFIRMATIONS_LIST) < 3):
        raise Exception('Please add at least 3 values to config.AFFIRMATIONS_LIST')
    
    return random.sample(config.AFFIRMATIONS_LIST, 3)


def build_message_body(aff_list: list) -> str:
     """
     function to build message body with affirmations and to/from names
     
     :return: message body as string
     """ 
     body = 'Good morning, {to_name}!\nHere are your daily affirmations: \n\n{first}\n{second}\n{third} \n\nHave a great day!\n\n-{from_name}'.format(
        to_name=config.TO_NAME, first=aff_list[0], second=aff_list[1], third=aff_list[2], from_name=config.FROM_NAME)
     return body


def handle_message(message_body: str, account_sid: str, auth_token: str) -> str:
    """
     function to handle Twilio API sending of message
     
     :return: message body as string
     """ 
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=message_body,
            from_=config.SOURCE_NUMBER,
            to=config.TARGET_NUMBER
        )
    return message.sid

if __name__ == '__main__':
    # manage environment variables with Twilio credentials
    load_dotenv()
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    
    try:
        # Get random sample of 3 affirmations and build message body
        selections = get_affirmations()
        # build the SMS message body
        message_body = build_message_body(selections)

        # send the message through Twilio API
        sid = handle_message(message_body=message_body, 
                                account_sid=account_sid,
                                auth_token=auth_token)
        print(sid)
        
    except Exception as e:
        print(str(e))
        
