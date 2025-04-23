from machine import Pin, PWM
import time

# Setup for AM312 PIR sensor
pir_sensor = Pin(14, Pin.IN)  # VOUT pin of AM312 to GPIO 14

# Setup for LED
led_pwm = PWM(Pin(13))       # GPIO pin connected to LED
led_pwm.freq(1000)           # Set PWM frequency to 1kHz
led_pwm.duty_u16(0)          # Start with LED off

# State variables
led_on = False               # Flag for LED state
motion_timeout = 10          # Time to keep LED on after motion stops (seconds)
last_motion_time = 0         # Time of last detected motion
inverted_led = True          # Set to TRUE if LED gets dimmer with higher PWM values

# Function to get timestamp
def get_timestamp():
    return time.time()

# Function to log messages with timestamp
def log_message(message):
    timestamp = get_timestamp()
    print(f"{timestamp}: {message}")

# More efficient gamma correction with fewer lookup values
gamma = 2.2
gamma_steps = 10  # Use fewer steps for efficiency
gamma_table = {}
for i in range(0, 101, gamma_steps):
    # Map 0-100 to 0-65535 for PWM
    gamma_table[i] = int(((i / 100.0) ** gamma) * 65535)

# Faster gamma correction function using percent-based values
def set_led_brightness(percent):
    # Ensure percent is within 0-100
    percent = max(0, min(100, percent))
    
    # Get nearest key in gamma table
    key = (percent // gamma_steps) * gamma_steps
    corrected_duty = gamma_table.get(key, int(((percent / 100.0) ** gamma) * 65535))
    
    if inverted_led:
        led_pwm.duty_u16(65535 - corrected_duty)
    else:
        led_pwm.duty_u16(corrected_duty)

# Function to smoothly fade in the LED (turn on)
def fade_in(steps=10, fade_time=0.01):
    for i in range(0, 101, steps):
        set_led_brightness(i)
        time.sleep(fade_time)
    
    # Ensure LED is fully on at the end
    set_led_brightness(100)
    log_message("LED on")

# Function to smoothly fade out the LED (turn off)
def fade_out(steps=10, fade_time=0.01):
    for i in range(100, -1, -steps):
        set_led_brightness(i)
        time.sleep(fade_time)
    
    # Ensure LED is fully off at the end
    set_led_brightness(0)
    log_message("LED off")

# Function to completely turn off the LED
def led_off():
    set_led_brightness(0)

# AM312 motion detection with original reliable debounce logic
def check_motion():
    raw_state = pir_sensor.value()
    
    # Proven debounce algorithm - take 3 readings
    if raw_state == 1:
        # Confirm with additional readings
        time.sleep(0.01)
        if pir_sensor.value() == 1:
            time.sleep(0.01)
            if pir_sensor.value() == 1:
                return True
    
    return False

# Main loop
try:
    log_message("AM312 Motion Detection System Started")
    led_off()
    
    # Brief stabilization - AM312 typically only needs 5-10 seconds
    log_message("Waiting for AM312 sensor to stabilize...")
    time.sleep(10)  # Adjusted to 10 seconds for better stability
    
    log_message("System ready!")
    
    while True:
        current_time = get_timestamp()
        
        # Check for motion with proven reliable debouncing
        if check_motion():
            # Motion detected - update the last motion time
            last_motion_time = current_time
            
            # If LED is off, turn it on
            if not led_on:
                log_message("Motion detected")
                fade_in()
                led_on = True
        
        # If LED is on, check if it's time to turn it off
        if led_on and (current_time - last_motion_time > motion_timeout):
            log_message("Motion timeout")
            fade_out()
            led_on = False
        
        time.sleep(0.05)  # Slightly faster checking for better responsiveness

except KeyboardInterrupt:
    log_message("Keyboard interrupt detected")
    led_off()
except Exception as e:
    log_message(f"Error: {e}")
    led_off()