import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

def MOTION(PIR_PIN):
    print("Motion Detected")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)

print("PIR Module Test (CTRL+C to exit)")
time.sleep(4)
print("Ready")

try:
    while True:
        if GPIO.input(PIR_PIN):
            MOTION(LED_PIN)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
