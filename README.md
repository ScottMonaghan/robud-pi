# robud-pi
Ro-Bud - Lovable, Accessible, Autonomous Companion (on the Raspberry Pi!)

# Set-up Steps (draft outline)
 - [X] Install 64bit RaspberryPi OS (for tensorflow)
   - hostname: robud.local
   - username: robud
   - password: your choice
 - [x] Clone repo - git clone https://github.com/ScottMonaghan/robud-pi.git
   - [x] Rename folder - mv robud-pi robud
   - [x] PYTHONPATH to robud source 
     - Add line to /home/robud/.bashrc - export PYTHONPATH="${PYTHONPATH}:/home/robud"
     - log out and log back in
 - [] Update pip3 install update pip
 - [x] Install VSCODE - sudo apt install code
 - [X] Install Mosquitto - sudo apt install mosquitto mosquitto-clients
 - [x] Configure mosquitto
   - sudo nano /etc/mosquitto/mosquitto.conf
   - Add these lines and save
     - allow_anonymous true
     - listener 1883 0.0.0.0
   - sudo systemctl restart moquitto.service
 - [X] Install paho.mqtt pip install paho-mqtt
 - [X] Install OpenCV - sudo apt install python3-opencv -y
 - [X] Install TensorFlow 2.10 - https://github.com/PINTO0309/Tensorflow-bin
     - Follow Example of Python 3.x + Tensorflow v2 series
     - use CPVER=39 (CircuitPython 3.9)
 - [X] Install eSpeak-ng - sudo apt-get install espeak-ng
 - [X] Install Librosa - pip install librosa
 - [x] Install Vosk
   - [x] pip3 install vosk
   - [x] navigate to ~/robud/robud/ai/stt/models (create folder if not created)
   - [x] If not already in repo, download Small English Model
     - wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
     - unzip vosk-model-small-en-us-0.15.zip
     - rm vosk-model-small-en-us-0.15.zip
   - [x] If not already in repo, download Speaker Identification Model
     - wget https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip
     - unzip vosk-model-spk-0.4.zip
     - rm vosk-model-spk-0.4.zip
 - [x] Install Blinka - pip3 install Adafruit-Blinka
 - [x] Install adafruit_motorkit - pip3 install adafruit-circuitpython-motorkit
 - [x] Install adafruit_servokit - pip3 install adafruit-circuitpython-servokit
 - [ ] Install portaudio19-dev library  sudo apt install portaudio19-dev
 - [x] Install pyaudio - pip3 install pyaudio
 - [x] Install pytweening - pip install pytweening
 - [x] Install bno055 -  pip3 install adafruit-circuitpython-bno055
 - [x] Update /boot/config.txt with following for bno0##: dtparam=i2c_arm_baudrate=400000
   - bno055 will crash i2c without this (https://learn.adafruit.com/raspberry-pi-i2c-clock-stretching-fixes)
 - [x] Install adafruit-circuitpython-vl53l0x (time-of-flight) - pip3 install adafruit-circuitpython-vl53l0x
 - ~[x] Install HC S404 Ultrasonic driver - pip3 install adafruit-circuitpython-hcsr04~ (ultrasonic sensors not integrated yet)
 - [x] Install VNC Server - sudo apt-get install realvnc-vnc-server
 - [x] Configure VNC Server 
   - sudo raspi-config
   - enable VNC
   - set VNC resolution
 - [x] Blink Test 1 - hook up to a monitor and see you get robud blinking if you run robud_face.py
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
    - [x] set up graphical autostart
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
    - [x] Blink Test 2 (start up test)
      - Hook up pi to monitor, keyboard & mouse, and restart. After a few min, RoBud's eyes should be looking around. CTRL-F to exit full scren.
    - [x] Blink Test 3 (VNC test)
      - Disconnect all HDMI cables from pi
      - Restart Pi and VNC to robud.local (or direct pi IP) RoBud's eyes should be looking around. 
      - Resolution should be your configured CTRL-F to exit full scren.
      
      






