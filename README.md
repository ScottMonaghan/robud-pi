# robud-pi
Ro-Bud - Lovable, Accessible, Autonomous Companion (on the Raspberry Pi!)

# Set-up Steps (draft outline)
 - [X] Install 64bit RaspberryPi OS (for tensorflow)
   - hostname: robud.local
   - username: robud
   - password: your choice 
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
   - wget https://github.com/MycroftAI/precise-data/blob/models/hey-mycroft.pb -P /home/robud/robud/ai/wakeword_detection/models/hey-mycroft.pb
 - [X] Install Coqui STT
   - wget https://github.com/coqui-ai/STT/releases/download/v1.4.0/stt-1.4.0-cp39-cp39-linux_aarch64.whl
   - pip install stt-1.4.0-cp39-cp39-linux_aarch64.whl
 - [x] Install Blinka - pip3 install Adafruit-Blinka
 - [x] Install adafruit_motorkit - pip3 install adafruit-circuitpython-motorkit
 - [x] Install adafruit_servokit - pip3 install adafruit-circuitpython-servokit
 - [x] Install pyaudio (installed as MyCroft Precise preq)
 - [x] Install pytweening - pip install pytweening
 - [x] Install bno055 -  pip3 install adafruit-circuitpython-bno055
 - [x] Install adafruit-circuitpython-vl53l0x (time-of-flight) - pip3 install adafruit-circuitpython-vl53l0x
 - [x] Install HC S404 Ultrasonic driver - pip3 install adafruit-circuitpython-hcsr04
 - [x] Install VNC Server - sudo apt-get install realvnc-vnc-server
 - [x] Configure VNC Server 
   - sudo raspi-config
   - enable VNC
   - set VNC resolution
 - [x] Clone repo - git clone https://github.com/ScottMonaghan/robud-pi.git
 - [x] Rename folder - mv robud-pi robud
 - [x] PYTHONPATH to robud source 
   - Add line to /home/robud/.bashrc - export PYTHONPATH="${PYTHONPATH}:/home/robud"
   - log out and log back in
 - [x] Install VSCODE - sudo apt install code
 - [x] Configure mosquitto
   - sudo nano /etc/mosquitto/mosquitto.conf
   - Add these lines and save
     - allow_anonomous true
     - listener 1883 0.0.0.0
   - sudo systemctl restart moquitto.service
 - [x] Blink Test 
   - python3 /home/robud/robud/robud_face/robud_face.py
   - ctrl-F to exit fullscreen
 - [x] Install Adafruit Platform Detect - pip3 install Adafruit-PlatformDetect
 - [x] Disable Hardware Accelleration on VSCODE - https://ratticon.com/how-to-fix-slow-visual-studio-code-on-raspberry-pi-4/
 - [ ] Set up UDEV rules so python can access respeaker through USB
   - sudo nano /etc/udev/rules.d/60-respeaker.rules
   - add line
     - SUBSYSTEM=="usb", ATTR{idProduct}=="0018", ATTR{idVendor}=="2886", MODE:="0666"
   - sudo systemctl restart udev
   - reconnect respeaker
