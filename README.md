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
 - [x] ~~Install MyCroft Precise~~
   - ~~sudo apt install portaudio19-dev python3-pyaudio~~
   - ~~wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_aarch64.tar.gz~~
   - ~~tar xvf precise-engine_0.3.0_aarch64.tar.gz~~
   - ~~sudo pip3 install precise-runner~~
   - ~~wget https://github.com/MycroftAI/precise-data/blob/models/hey-mycroft.pb -P /home/robud/robud/ai/wakeword_detection/models/~~
   - ~~wget https://github.com/MycroftAI/precise-data/blob/models/hey-mycroft.pb.params -P /home/robud/robud/ai/wakeword_detection/models/~~
 - [x] ~~Install Coqui STT~~
   - ~~wget https://github.com/coqui-ai/STT/releases/download/v1.4.0/stt-1.4.0-cp39-cp39-linux_aarch64.whl~~
   - ~~pip install stt-1.4.0-cp39-cp39-linux_aarch64.whl~~
 - [x] Install Vosk
   - [x] pip3 install vosk
   - [x] navigate to ~/robud/ai/stt/models (create folder if not created)
   - [x] Download Small English Model
     - wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
     - unzip vosk-model-small-en-us-0.15.zip
     - rm vosk-model-small-en-us-0.15.zip
   - [x] Download Speaker Identification Model
     - wget https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip
     - unzip vosk-model-spk-0.4.zip
     - rm vosk-model-spk-0.4.zip
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
 - [x] Set up UDEV rules so python can access respeaker through USB
   - sudo nano /etc/udev/rules.d/60-respeaker.rules
   - add line
     - SUBSYSTEM=="usb", ATTR{idProduct}=="0018", ATTR{idVendor}=="2886", MODE:="0666"
   - sudo systemctl restart udev
   - reconnect respeaker
  - [x] Set up Services
    - sudo cp /home/robud/robud/services/robud.motors.motors.service /etc/systemd/system
    - ~~sudo cp /home/robud/robud/services/robud.robud_audio.robud_audio.service  /etc/systemd/system~~
    - sudo cp /home/robud/robud/services/robud.robud_face.robud_face_animator.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.robud_head.robud_head_animator.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.robud_logging.robud_logger.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.robud_questions.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.robud_voice_text_input.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.sensors.orientation.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.sensors.tof.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.robud_state.robud_state_manager.service /etc/systemd/system
    - sudo cp /home/robud/robud/services/robud.sensors.camera.service /etc/systemd/system
    - sudo systemctl daemon-reload
    - sudo systemctl enable [each service unit file]
    - The following services need changes still to work RPi 12-Jan-2023
      - pulseaudio.service
      - robud.ai.object_detection.service
      - robud.ai.stt.service
      - robud.ai.wakeword_detection.service
      - robud.sensors.light_level.service
      - robud.sensors.odometry.service
      - robud.sensors.ultrasonics.service
    - [ ] set up graphical autostart
      - mkdir /home/robud/.config/autostart
      - ~~cp /home/robud/robud/robud_startup.sh /home/robud/.config/autostart~~
      - sudo nano /home/robud/.config/autostart/robud.desktop
        - 
        ```
        [Desktop Entry]
        Name=robud
        Exec=/home/robud/robud/robud_startup.sh
        Terminal=false
        Type=Application
        ```
      
      






