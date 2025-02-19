import RPi.GPIO as GPIO
import time
import threading

# GPIO pin setup
TRIG = 23          # Ultrasonic Trigger pin
ECHO = 24          # Ultrasonic Echo pin
TOUCH_SENSOR_PIN = 18  # Touch Sensor pin
SERVO_PIN_1 = 13   # First Servo pin
SERVO_PIN_2 = 12   # Second Servo pin
SERVO_PIN_3 = 26   # Third Servo pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)
GPIO.setup(SERVO_PIN_3, GPIO.OUT)

# Initialize servos
p1 = GPIO.PWM(SERVO_PIN_1, 50)  # PWM frequency is 50Hz for servo 1
p2 = GPIO.PWM(SERVO_PIN_2, 50)  # PWM frequency is 50Hz for servo 2
p3 = GPIO.PWM(SERVO_PIN_3, 50)  # PWM frequency is 50Hz for servo 3

p1.start(0)  # Start with servos stopped
p2.start(0)  # Start with servos stopped
p3.start(0)  # Start with servos stopped

# Function to measure distance
def measure_distance():
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:", distance, "cm")
        time.sleep(1)

# Function to move the servos
def move_servos():
    print("Moving servos!")
    # Rotate all servos to 90 degrees
    p1.ChangeDutyCycle(5)   # Rotate servo 1 to 90 degrees
    p2.ChangeDutyCycle(5)   # Rotate servo 2 to 90 degrees
    p3.ChangeDutyCycle(5)   # Rotate servo 3 to 90 degrees
    time.sleep(1)           # Hold position for a moment

    # Rotate all servos to 180 degrees
    p1.ChangeDutyCycle(10)  # Rotate servo 1 to 180 degrees
    p2.ChangeDutyCycle(10)  # Rotate servo 2 to 180 degrees
    p3.ChangeDutyCycle(10)  # Rotate servo 3 to 180 degrees
    time.sleep(1)           # Hold position for a moment

    # Rotate all servos back to 0 degrees
    p1.ChangeDutyCycle(2.5)  # Rotate servo 1 back to 0 degrees
    p2.ChangeDutyCycle(2.5)  # Rotate servo 2 back to 0 degrees
    p3.ChangeDutyCycle(2.5)  # Rotate servo 3 back to 0 degrees
    time.sleep(1)            # Hold position for a moment

    # Stop all servos to prevent jitter
    p1.ChangeDutyCycle(0)  # Stop servo 1
    p2.ChangeDutyCycle(0)  # Stop servo 2
    p3.ChangeDutyCycle(0)  # Stop servo 3
    print("Servos stopped.")

# Function to monitor the touch sensor
def touch_sensor_monitor():
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.LOW:  # Touch detected
            move_servos()  # Move servos on touch
            time.sleep(1)  # Prevent multiple triggers
        time.sleep(0.1)  # Short delay to prevent busy-waiting

# Start threads
distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True  # Ensure thread exits when main program does
distance_thread.start()

touch_thread = threading.Thread(target=touch_sensor_monitor)
touch_thread.daemon = True  # Ensure thread exits when main program does
touch_thread.start()

try:
    while True:
        time.sleep(1)  # Main thread sleeps to keep the script running

except KeyboardInterrupt:
    print("Stopping...")
    p1.stop()
    p2.stop()
    p3.stop()
    GPIO.cleanup()
