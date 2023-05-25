from robud.robud_chatbot.chatgpt.robud_chatgpt_config import (
    OPENAI_KEY
    ,OPENAI_MODEL
    ,OPENAI_TIMEOUT
    ,RETRY_SLEEP_DURATION
    ,CHAT_HISTORY_DIRECTORY
    ,OPENING_SYSTEM_MESSAGE_CONTENT
    ,OPENING_ROBUD_MESSAGE_CONTENT
    ,MQTT_BROKER_ADDRESS
    ,LOGGING_LEVEL
    ,CLOSING_ROBUD_MESSAGE_CONTENT
)
from robud.robud_chatbot.chatgpt.robud_chatgpt_common import (
    TOPIC_ROBUD_CHATGPT_NEW_CHAT
    ,TOPIC_ROBUD_CHATGPT_END_CHAT
    ,TOPIC_ROBUD_CHATGPT_RESPONSE_MESSAGE
    ,TOPIC_ROBUD_CHATGPT_SYSTEM_MESSAGE
    ,TOPIC_ROBUD_CHATGPT_USER_MESSAGE
)
import traceback
import openai
openai.api_key = OPENAI_KEY
from time import sleep
from datetime import datetime
import os
import paho.mqtt.client as mqtt
import random
import logging
import argparse
from robud.robud_logging.MQTTHandler import MQTTHandler


#initialize logger
random.seed()

MQTT_CLIENT_NAME = "robud_chatgpt.py" + str(random.randint(0,999999999))

TOPIC_ROBUD_LOGGING_LOG = "robud/robud_logging/log"
TOPIC_ROBUD_LOGGING_LOG_SIGNED = TOPIC_ROBUD_LOGGING_LOG + "/" + MQTT_CLIENT_NAME
TOPIC_ROBUD_LOGGING_LOG_ALL = TOPIC_ROBUD_LOGGING_LOG + "/#"

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--Output", help="Log Ouput Prefix", default="logs/robud_chatgpt_log_")
args = parser.parse_args()

#initialize logger
logger=logging.getLogger()
file_path = args.Output + datetime.now().strftime("%Y-%m-%d") + ".txt"
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)
log_file = open(file_path, "a",encoding='UTF-8')
myHandler = MQTTHandler(hostname=MQTT_BROKER_ADDRESS, topic=TOPIC_ROBUD_LOGGING_LOG_SIGNED, qos=2, log_file=log_file)
myHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(filename)s: %(message)s'))
logger.addHandler(myHandler)
logger.level = LOGGING_LEVEL

class chat_message(dict):
    ROLE_SYSTEM = "system"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    KEY_ROLE = "role"
    KEY_CONTENT = "content"
    
    def __init__(self,role:str = "", content:str = "", message_dict:dict = None) -> None:
            super().__init__()
            if message_dict is not None:
                 self.update(message_dict)
            else:
                self[chat_message.KEY_ROLE] = role
                self[chat_message.KEY_CONTENT] = content

def get_chat_response():
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL
        , messages = messages
        , request_timeout = OPENAI_TIMEOUT
    )
    response_message = chat_message(role=response['choices'][0]['message']['role'],content=response['choices'][0]['message']['content'])
    return response_message


opening_message = chat_message(
        role=chat_message.ROLE_ASSISTANT
        ,content=OPENING_ROBUD_MESSAGE_CONTENT 
)

retry_message = chat_message(
     role=chat_message.ROLE_ASSISTANT
     ,content="One moment, I'm having trouble reaching chatgpt. Let me try agian."
)

messages=[]

client_userdata = {
    "messages":messages
    ,"chat_history_filename":""
    ,"user_prompt":""
    ,"chat_is_active":False
}

def on_message_new_chat(client:mqtt.Client, userdata, message):
    logger.info("New Chat request received. Clearing old chat & creating new.")
    messages:list = userdata["messages"]
    messages.clear()
    messages.append(
        chat_message(
            role=chat_message.ROLE_SYSTEM
            ,content=OPENING_SYSTEM_MESSAGE_CONTENT
        )
    )
    userdata["chat_history_filename"] = "chat_messages_" + datetime.now().strftime("%Y-%m-%d") + ".txt"    
    userdata["user_prompt"]="test"
    print("user_prompt: " +userdata["user_prompt"])

    messages.append(opening_message)
    logger.info("Robud: " + opening_message[chat_message.KEY_CONTENT])
    client.publish(topic=TOPIC_ROBUD_CHATGPT_RESPONSE_MESSAGE, payload=opening_message[chat_message.KEY_CONTENT])
    userdata["chat_is_active"] = True

def on_message_user_message(client:mqtt.Client, userdata, message):
    logger.info("New user message received: " + userdata["user_prompt"])
    if userdata["chat_is_active"]:
        userdata["user_prompt"] = message.payload.decode()
        logger.info("New user message received: " + userdata["user_prompt"])
        messages = userdata["messages"]
        user_prompt = userdata["user_prompt"]
        while True:
            try:
                messages.append(chat_message(role=chat_message.ROLE_USER, content=user_prompt))
                response_message = get_chat_response()
                break
            except openai.error.Timeout:
                print("RoBud: " + retry_message[chat_message.KEY_CONTENT])
                messages.append(retry_message)
                logger.info("Robud: " + response_message[retry_message.KEY_CONTENT])
                client.publish(topic=TOPIC_ROBUD_CHATGPT_RESPONSE_MESSAGE, payload=retry_message[chat_message.KEY_CONTENT])
                sleep(RETRY_SLEEP_DURATION)
        messages.append(response_message)
        logger.info("Robud: " + response_message[chat_message.KEY_CONTENT])
        client.publish(topic=TOPIC_ROBUD_CHATGPT_RESPONSE_MESSAGE, payload=response_message[chat_message.KEY_CONTENT])

        if not os.path.exists(CHAT_HISTORY_DIRECTORY):
            os.makedirs(CHAT_HISTORY_DIRECTORY)
        f = open(CHAT_HISTORY_DIRECTORY + "/" + userdata["chat_history_filename"], "w")
        f.write(str(messages))
        f.close()

def on_message_end_chat(client:mqtt.Client, userdata, message):
    logger.info("End Chat request received. Clearing old chat & creating new.")
    if userdata["chat_is_active"]:
        messages:list = userdata["messages"]
        messages.clear()
        messages.append(
            chat_message(
                role=chat_message.ROLE_SYSTEM
                ,content=OPENING_SYSTEM_MESSAGE_CONTENT
            )
        )
        userdata["user_prompt"]=""

        closing_message = chat_message(role=chat_message.ROLE_ASSISTANT, content=CLOSING_ROBUD_MESSAGE_CONTENT)
        messages.append(closing_message)
        logger.info("Robud: " + closing_message[chat_message.KEY_CONTENT])
        client.publish(topic=TOPIC_ROBUD_CHATGPT_RESPONSE_MESSAGE, payload=closing_message[chat_message.KEY_CONTENT])
        if not os.path.exists(CHAT_HISTORY_DIRECTORY):
            os.makedirs(CHAT_HISTORY_DIRECTORY)
        f = open(CHAT_HISTORY_DIRECTORY + "/" + userdata["chat_history_filename"], "w")
        f.write(str(messages))
        f.close()
        userdata["chat_history_filename"] = ""   
        userdata["chat_active"] = False                                                                              

mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_NAME,userdata=client_userdata)
mqtt_client.connect(MQTT_BROKER_ADDRESS)
logger.info('MQTT Client Connected')
mqtt_client.subscribe(TOPIC_ROBUD_CHATGPT_END_CHAT)
mqtt_client.subscribe(TOPIC_ROBUD_CHATGPT_NEW_CHAT)
mqtt_client.subscribe(TOPIC_ROBUD_CHATGPT_SYSTEM_MESSAGE)
mqtt_client.subscribe(TOPIC_ROBUD_CHATGPT_USER_MESSAGE)

mqtt_client.message_callback_add(TOPIC_ROBUD_CHATGPT_NEW_CHAT,on_message_new_chat)
mqtt_client.message_callback_add(TOPIC_ROBUD_CHATGPT_USER_MESSAGE,on_message_user_message)
mqtt_client.message_callback_add(TOPIC_ROBUD_CHATGPT_END_CHAT,on_message_end_chat)

logger.info('Waiting for messages...')
try: 
    mqtt_client.loop_forever()
except Exception as e:
    logger.critical(str(e) + "\n" + traceback.format_exc())
except KeyboardInterrupt:
    logger.info("Exited with Keyboard Interrupt")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
# Begin chat

# messages = [
#     chat_message(
#           role=chat_message.ROLE_SYSTEM
#           ,content=OPENING_SYSTEM_MESSAGE_CONTENT
#     )
# ]

# chat_history_filename = "chat_messages_" + datetime.now().strftime("%Y-%m-%d") + ".txt"    
# user_prompt=""

# messages.append(opening_message)
# logger.info("Robud: " + opening_message[chat_message.KEY_CONTENT])
# while True:
#     try:
#         if messages[-1] != retry_message: #if last message was retry_message try again
#             user_prompt = input("Prompt: ")
#         if user_prompt != "":
#             messages.append(chat_message(role=chat_message.ROLE_USER, content=user_prompt))
#             response_message = get_chat_response()
#         if not os.path.exists(CHAT_HISTORY_DIRECTORY):
#             os.makedirs(CHAT_HISTORY_DIRECTORY)
#         f = open(CHAT_HISTORY_DIRECTORY + "/" + chat_history_filename, "w")
#         f.write(str(messages))
#         f.close()
#     except openai.error.Timeout:
#         print("RoBud: " + retry_message[chat_message.KEY_CONTENT])
#         messages.append(retry_message)
#         sleep(RETRY_SLEEP_DURATION)
#     except Exception as e:
#         print(str(e) + "\n" + traceback.format_exc())
        




