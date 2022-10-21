# robud-pi
Ro-Bud - Lovable, Accessible, Autonomous Companion (on the Raspberry Pi!)

# Set-up Steps (draft outline)
 - [X] Install 64bit RaspberryPi OS (for tensorflow)
 - [X] Install Mosquitto - sudo apt install mosquitto mosquitto-clients
 - [X] Install paho.mqtt pip install paho-mqtt
 - [X] Install OpenCV - sudo apt install python3-opencv -y
 - [X] Install TensorFlow 2.10 - https://github.com/PINTO0309/Tensorflow-bin
 - [X] Install eSpeak-ng - sudo apt-get install espeak-ng
 - [X] Install Librosa - pip install librosa
 - [X] Install MyCroft Precise
   - sudo apt install portaudio19-dev python3-pyaudio
   - wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_aarch64.tar.gz
   - tar xvf precise-engine_0.3.0_aarch64.tar.gz
   - sudo pip3 install precise-runner
   - TODO: Download models
 - [X] Install Coqui STT
   - wget https://github.com/coqui-ai/STT/releases/download/v1.4.0/stt-1.4.0-cp39-cp39-linux_aarch64.whl
   - pip install stt-1.4.0-cp39-cp39-linux_aarch64.whl
 - [ ] Install Blinka
 - [ ] Install adafruit_motorkit
 - [ ] Install adafruit_servokit
 - [x] Install pyaudio (installed as MyCroft Precise preq)
 - [ ] Install pytweening
 - [ ] Add additional requirements
