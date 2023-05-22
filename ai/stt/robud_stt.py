#Need to add timeout so audio doesn't keep processing if it keeps detecting voice. ~ 5 sec seems appropriate.

from robud.ai.stt.stt_config import (
    MQTT_BROKER_ADDRESS
    ,STT_UTTERANCE_TIMEOUT
    ,SAMPLE_RATE
)
from robud.ai.stt.stt_common import(
    TOPIC_STT_OUTPUT,
    TOPIC_STT_REQUEST
)

import random
import logging
import argparse
from robud.robud_logging.MQTTHandler import MQTTHandler
from datetime import datetime
import os
import traceback
import sys
import paho.mqtt.client as mqtt
from time import monotonic
from vosk import Model, KaldiRecognizer
import os.path
from robud.robud_audio.robud_audio_common import (
    TOPIC_AUDIO_INPUT_DATA
    ,TOPIC_SPEECH_INPUT_COMPLETE
)
import json

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
    input_audio = b''

    def on_message_stt_request(client:mqtt.Client, userdata,message):
        # ToDo
        #   [x] Modify from STT to VOSK
        logger.info("stt request received")
        #reset recognizer for new input
        rec:KaldiRecognizer = userdata["rec"]
        rec.Reset()
        userdata["recording_start"] = monotonic()
        #userdata["stt_triggered"] = True
        # model:stt.Model = userdata["model"]
        # userdata["stream_context"] = model.createStream()
        #model = userdata["model"]
        #userdata["rec"] = KaldiRecognizer(model, SAMPLE_RATE) 
        #userdata["input_audio"] = b''
        
        return
    
    def on_message_speech_input_data(client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        rec:KaldiRecognizer = userdata["rec"]
        #clear rec if more than timeout
        if monotonic() - userdata["recording_start"] > STT_UTTERANCE_TIMEOUT:
            rec.Reset()
            userdata["recording_start"] = monotonic()
        rec.AcceptWaveform(message.payload)

    def on_message_speech_input_complete(client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        if userdata["rec"]:
            logger.info("Speech input Complete. Processing...")
            rec:KaldiRecognizer = userdata["rec"]
            result = json.loads(rec.Result())
            print(result)
            text = result["text"]
            logging.info("Recognized: %s" % text)
            client.publish(TOPIC_STT_OUTPUT, text)  
        return

    # Load Vosk model
    model = Model(lang="en-us")
    rec = KaldiRecognizer(model, SAMPLE_RATE) 
    recording_start = monotonic()

    client_userdata = {
        "rec":rec
        ,"recording_start":recording_start
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