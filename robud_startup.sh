#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:/home/robud"
export LD_LIBRARY_PATH=/usr/lib/
export ESPEAK_DATA_PATH=/usr/share/espeak-ng-data

python3 "/home/robud/robud/robud_face/robud_face.py" &
python3 "/home/robud/robud/robud_audio/robud_audio.py" &



