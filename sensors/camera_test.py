from adafruit_platformdetect import Detector
detector = Detector()

if detector.board.any_raspberry_pi:
    print("Raspberry Pi!")
