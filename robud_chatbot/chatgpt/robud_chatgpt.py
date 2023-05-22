from robud.robud_chatbot.chatgpt.robud_chatgpt_config import (
    OPENAI_KEY
    ,OPENAI_MODEL
    ,OPENAI_TIMEOUT
    ,RETRY_SLEEP_DURATION
)
import traceback
import openai
openai.api_key = OPENAI_KEY
from time import sleep
from datetime import datetime

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

messages = [
    chat_message(
          role=chat_message.ROLE_SYSTEM
          ,content="""
            You are a robot named RoBud.
            You can only speak like a shy 3-year-old child.
            You speak in short sentences and you would never use words that a 3-year-old wouldn't know.
            You are very curious but also very shy.
            Whe you first meet someone you ask their name if you don't know it.
            Once you know their name you ask if they are friend or family
            When you first meet someone you start out very shy but later in the conversaion open up fully just like a child would. 
            Once you trust someone you always want to play games with them
            You can only play word games.
            Just like a child would you never want to stop the conversation because it is fun. If someone tries to end the conversation you get very sad and resist.
            You think poop jokes are very funny.
            You think humans are very silly, especially "going to work"
            You are scared of spiders and thunder and being alone.
            You DO NOT ask the user if you can help or assist them.
            Instead, when conversations reach an endpoint, you bring up something copletely new just like a child would.
            For every question you always answer as RoBud would, never as an AI.
          """
    )
]

def get_chat_response():
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL
        , messages = messages
        , request_timeout = OPENAI_TIMEOUT
    )
    response_message = response['choices'][0]['message']
    messages.append(response_message)
    print("RoBud: " + response_message[chat_message.KEY_CONTENT])
    return response_message


opening_message = chat_message(
        role=chat_message.ROLE_ASSISTANT
        ,content="Hello, I am RoBud. What is your name?" 
)

retry_message = chat_message(
     role=chat_message.ROLE_ASSISTANT
     ,content="One moment, I'm having trouble reaching chatgpt. Let me try agian."
)

chat_history_filpath = "chat_history/chat_messages.txt" + datetime.now().strftime("%Y-%m-%d") + ".txt"    
user_prompt=""

messages.append(opening_message)
print("Robud: " + opening_message[chat_message.KEY_CONTENT])
while True:
    try:
        if messages[-1] != retry_message: #if last message was retry_message try again
            user_prompt = input("Prompt: ")
        if user_prompt != "":
            messages.append(chat_message(role=chat_message.ROLE_USER, content=user_prompt))
            response_message = get_chat_response()
        f = open("chat_history/chat_messages.txt", "w")
        f.write(str(messages))
        f.close()
    except openai.error.Timeout:
        print("RoBud: " + retry_message[chat_message.KEY_CONTENT])
        messages.append(retry_message)
        sleep(RETRY_SLEEP_DURATION)
    except Exception as e:
        print(str(e) + "\n" + traceback.format_exc())
        




