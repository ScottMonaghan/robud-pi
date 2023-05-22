#wakeword_detection.py
#Subscribes to robud/ai/stt/output
#If wakeword found, text after wakeword is published if applicable

from ast import Bytes
from pyaudio import PyAudio, paInt16, paContinue, Stream
from io import BytesIO
#from precise_runner import PreciseEngine
from precise_runner.runner import TriggerDetector, PreciseEngine
from robud.ai.wakeword_detection.wakeword_detection_config import(
    LOGGING_LEVEL
    , MQTT_BROKER_ADDRESS
    , WAKEWORD_PATTERN
)
from robud.ai.wakeword_detection.wakeword_detection_common import(
     TOPIC_WAKEWORD_DETECTED
)
from robud.robud_audio.robud_audio_common import (
    TOPIC_AUDIO_INPUT_DATA
)

from robud.ai.stt.stt_common import (
    TOPIC_STT_OUTPUT
)

import random
import logging
import argparse
from robud.robud_logging.MQTTHandler import MQTTHandler
from datetime import datetime
import os
import paho.mqtt.client as mqtt
from time import sleep
import traceback
import sys
import re
import pickle
import struct

random.seed()

MQTT_CLIENT_NAME = "wakeword_detection.py" + str(random.randint(0,999999999))

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
    client_userdata = {}
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_NAME,userdata=client_userdata)
    
    # [ ] Replace below with callback & full handling for stt
    # [ ] Republish full text with wakeword

    def on_message_stt_output(client:mqtt.Client, userdata, message):
        stt_output = message.payload.decode()
        logger.debug("stt output received: " + stt_output)
        #pattern explanation 
        # r".*" -- 0 or more characters
        # then the wakeword pattern
        # r"\W* -- 0 or more non-word characters, usually a space 
        # (.*) -- 0 or more characters in a group so we can capture any text after the wakeworkd

        match:re.Match = re.match(r".*" + WAKEWORD_PATTERN + r"\W*(.*)",stt_output,re.IGNORECASE)
        if match is not None:
            logger.info("Wakeword Detected!")
            command = str(match.group(1))
            logger.info("Command: " + command)
            mqtt_client.publish(topic=TOPIC_WAKEWORD_DETECTED, payload=command,qos=0)
        else:
            logger.debug("No match detected")

    # def on_message_audio_input_data(client:mqtt.Client, userdata, message):
    #     if engine.proc: #this is the Popen external process run for the precise engine. It takes a bit to fully open so this prevents errors before it fully starts.
    #         chunk = message.payload
    #         handle_predictions(chunk)

    # def handle_predictions(chunk):
    #     """Check Precise process output"""
    #     prob = engine.get_prediction(chunk)
    #     if detector.update(prob):
    #        
    #        logger.info("Wakeword Detected!")

    #initialize mqtt client
    mqtt_client.connect(MQTT_BROKER_ADDRESS)
    logger.info('MQTT Client Connected')
    #[X]subscribe to STT datam -- mqtt_client.subscribe(TOPIC_AUDIO_INPUT_DATA)
    mqtt_client.subscribe(TOPIC_STT_OUTPUT)
    #[x]set callback -- mqtt_client.message_callback_add(TOPIC_AUDIO_INPUT_DATA, on_message_audio_input_data)  
    mqtt_client.message_callback_add(TOPIC_STT_OUTPUT, on_message_stt_output) 
    #[ ]log -- logger.info('Subscribed to ' + TOPIC_AUDIO_INPUT_DATA)
    logger.info('Subscribed to ' + TOPIC_STT_OUTPUT)
    
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
