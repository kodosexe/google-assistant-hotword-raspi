import snowboydecoder
import sys
import signal
import time
import logging
import RPi.GPIO as GPIO
from assistant import Assistant

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Pin 16 on RPi Hardware
ledPin = 23
GPIO.setup(ledPin, GPIO.OUT)

interrupted = False

logging.basicConfig()
logger = logging.getLogger("daemon")
logger.setLevel(logging.DEBUG)

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = sys.argv[1]
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
assistant = Assistant()


def detect_callback():
    detector.terminate()
    GPIO.output(ledPin, HIGH)
    assistant.assist()
    GPIO.output(ledPin, LOW)
    detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)


print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detect_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
