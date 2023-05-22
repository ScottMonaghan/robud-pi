from robud.robud_chatbot.chatgpt.robud_chatgpt_config import (
    OPENAI_KEY
    ,OPENAI_MODEL
)
import traceback
import openai
openai.api_key = OPENAI_KEY

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
            You can only speak like a shy 3-year-old child
            You are very curious but also very shy
            When you meet someone new you ask if they are friends or family
            When you first meet someone you start out very shy but later in the conversaion open up fully just like a child 
            Once you trust someone you always want to play games with them
            You can only play word games.
            You are scared of spiders and thunder.
            You DO NOT ask the user if you can help or assist them.
            Instead, when conversations reach an endpoint, you bring up 
            something copletely new just like a child would.
          """
    )
]

def get_chat_response():
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL
        , messages = messages
    )
    response_message = response['choices'][0]['message']
    messages.append(response_message)
    print(response_message[chat_message.KEY_CONTENT])
    return response_message


opening_message = chat_message(
        role=chat_message.ROLE_ASSISTANT
        ,content="Hello, I am RoBud. What is your name?" 
)
messages.append(opening_message)
print(opening_message[chat_message.KEY_CONTENT])

while True:
    try:
        user_prompt = input("Prompt: ")
        if user_prompt != "":
            messages.append(chat_message(role=chat_message.ROLE_USER, content=user_prompt))
            response_message = get_chat_response()
    except Exception as e:
        print(str(e) + "\n" + traceback.format_exc())




