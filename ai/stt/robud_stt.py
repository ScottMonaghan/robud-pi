from robud.ai.stt.stt_config import (
    MQTT_BROKER_ADDRESS 
    ,AUDIO_INPUT_INDEX 
    ,STT_MODEL_PATH
    ,STT_SCORER_PATH
    ,VAD_AGGRESSIVENESS
    ,SAMPLE_RATE

)
from robud.ai.stt.stt_common import(
    TOPIC_STT_OUTPUT,
    TOPIC_STT_REQUEST
)
#from robud.ai.stt.vadaudio import Audio, VADAudio
import random
import logging
import argparse
from robud.robud_logging.MQTTHandler import MQTTHandler
from datetime import datetime
import os
import traceback
import sys
import paho.mqtt.client as mqtt
import time
import stt
from vosk import Model, KaldiRecognizer
import numpy as np
#import pyaudio
import wave
import webrtcvad
#from halo import Halo
from scipy import signal
import threading, collections, queue, os.path
from robud.robud_voice.robud_voice_common import TOPIC_ROBUD_VOICE_TEXT_INPUT
from robud.robud_questions.robud_questions_common import TOPIC_QUESTIONS
import re #regular expressions
from robud.robud_audio.robud_audio_common import (
    TOPIC_AUDIO_INPUT_DATA,
    TOPIC_SPEECH_INPUT_DATA
    ,TOPIC_SPEECH_INPUT_COMPLETE
    ,TOPIC_AUDIO_OUTPUT_DATA
)
from robud.robud_state.robud_state_common import TOPIC_ROBUD_STATE

random.seed()

MQTT_CLIENT_NAME = "stt.py" + str(random.randint(0,999999999))

TOPIC_ROBUD_LOGGING_LOG = "robud/robud_logging/log"
TOPIC_ROBUD_LOGGING_LOG_SIGNED = TOPIC_ROBUD_LOGGING_LOG + "/" + MQTT_CLIENT_NAME
TOPIC_ROBUD_LOGGING_LOG_ALL = TOPIC_ROBUD_LOGGING_LOG + "/#"
LOGGING_LEVEL = logging.DEBUG

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--Output", help="Log Ouput Prefix", default="logs/robud_stt_log_")
args = parser.parse_args()

#initialize logger
logger=logging.getLogger()
file_path = args.Output + datetime.now().strftime("%Y-%m-%d") + ".txt"
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)
log_file = open(file_path, "a")
myHandler = MQTTHandler(hostname=MQTT_BROKER_ADDRESS, topic=TOPIC_ROBUD_LOGGING_LOG_SIGNED, qos=2, log_file=log_file)
myHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(filename)s: %(message)s'))
logger.addHandler(myHandler)
logger.level = LOGGING_LEVEL

try:
    # ToDo:
    #   [ ] Change to use VOSK
    #   [ ] Update trigger to any speech detection

    input_audio = b''

    def on_message_stt_request(client:mqtt.Client, userdata,message):
        # ToDo
        #   [ ] Modify from STT to VOSK
        logger.info("stt request received")
        userdata["stt_triggered"] = True
        # model:stt.Model = userdata["model"]
        # userdata["stream_context"] = model.createStream()
        model = userdata["model"]
        userdata["rec"] = KaldiRecognizer(model, SAMPLE_RATE) 
        userdata["input_audio"] = b''
        return
    
    def on_message_speech_input_data(client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        # ToDo
        #   [ ] Modify from STT to VOSK
        if userdata["stt_triggered"] and userdata["rec"]:
            #logger.debug("Speech input received")
            # stream_context:stt.Stream = userdata["stream_context"]
            # stream_context.feedAudioContent(np.frombuffer(message.payload, np.int16))
            userdata["input_audio"] = userdata["input_audio"] + message.payload
            rec = userdata["rec"]
            if rec.AcceptWaveform(message.payload):
                print (rec.Result())
            else:
               print(rec.PartialResult())
        return

    def on_message_speech_input_complete(client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        # ToDo
        #   [ ] Modify from STT to VOSK
        if userdata["stt_triggered"] and userdata["rec"]:
            logger.info("Speech input Complete. Processing...")
            # stream_context:stt.Stream = userdata["stream_context"]
            userdata["stt_triggered"] = False 
            rec:KaldiRecognizer = userdata["rec"]
            text = rec.Result()
            # text = stream_context.finishStream()
            # text = text.strip()
            logging.info("Recognized: %s" % text)
            client.publish(TOPIC_STT_OUTPUT, text)  
            #client.publish(TOPIC_AUDIO_OUTPUT_DATA, userdata["input_audio"])
        return

    # Load Vosk model
    model = Model(lang="en-us")
    rec = KaldiRecognizer(model, SAMPLE_RATE) 

    client_userdata = {
    #     "model":model
         "stt_triggered":False
         ,"input_audio":b''
         ,"model":model
         ,"rec":rec
    }
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_NAME,userdata=client_userdata)
    mqtt_client.connect(MQTT_BROKER_ADDRESS)
    logger.info('MQTT Client Connected')
    mqtt_client.subscribe(TOPIC_STT_REQUEST)
    mqtt_client.message_callback_add(TOPIC_STT_REQUEST,on_message_stt_request)
    mqtt_client.subscribe(TOPIC_AUDIO_INPUT_DATA)
    mqtt_client.message_callback_add(TOPIC_AUDIO_INPUT_DATA,on_message_speech_input_data)
    mqtt_client.subscribe(TOPIC_SPEECH_INPUT_COMPLETE)
    mqtt_client.message_callback_add(TOPIC_SPEECH_INPUT_COMPLETE,on_message_speech_input_complete)
    logger.info('Waiting for messages...')
    mqtt_client.loop_forever()
except Exception as e:
    logger.critical(str(e) + "\n" + traceback.format_exc())
except KeyboardInterrupt:
    logger.info("Exited with Keyboard Interrupt")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)