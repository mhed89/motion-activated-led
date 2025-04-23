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

# AM312 specific settings
am312_delay = 3              # AM312 has a typical 2-3 second delay after motion stops
debounce_time = 0.2          # Time in seconds for debounce

# Function to get timestamp
def get_timestamp():
    return time.time()

# Function to log messages with timestamp
def log_message(message):
    timestamp = get_timestamp()
    print(f"{timestamp}: {message}")

# Pre-compute gamma correction table for efficiency
gamma = 2.2
step = 1000  # Smaller step size for smoother fading
gamma_table = {}
for i in range(0, 65536, step):
    gamma_table[i] = int((i / 65535.0) ** gamma * 65535)

# Gamma correction function using lookup table
def gamma_correct(value):
    key = (value // step) * step
    return gamma_table.get(key, int((value / 65535.0) ** gamma * 65535))

# Function to smoothly fade in the LED (turn on)
def fade_in(led_pwm, step=1000, fade_time=0.003):
    if inverted_led:
        for raw_duty in range(65535, -1, -step):
            corrected_duty = gamma_correct(raw_duty)
            led_pwm.duty_u16(corrected_duty)
            time.sleep(fade_time)
    else:
        for raw_duty in range(0, 65536, step):
            corrected_duty = gamma_correct(raw_duty)
            led_pwm.duty_u16(corrected_duty)
            time.sleep(fade_time)
    
    # Ensure LED is fully on at the end
    if inverted_led:
        led_pwm.duty_u16(0)
    else:
        led_pwm.duty_u16(65535)
    
    log_message("LED faded in (turned ON)")

# Function to smoothly fade out the LED (turn off)
def fade_out(led_pwm, step=1000, fade_time=0.005):
    if inverted_led:
        for raw_duty in range(0, 65536, step):
            corrected_duty = gamma_correct(raw_duty)
            led_pwm.duty_u16(corrected_duty)
            time.sleep(fade_time)
    else:
        for raw_duty in range(65535, -1, -step):
            corrected_duty = gamma_correct(raw_duty)
            led_pwm.duty_u16(corrected_duty)
            time.sleep(fade_time)
    
    # Ensure LED is fully off at the end
    if inverted_led:
        led_pwm.duty_u16(65535)
    else:
        led_pwm.duty_u16(0)
    
    log_message("LED faded out (turned OFF)")

# Function to completely turn off the LED
def led_off():
    if inverted_led:
        led_pwm.duty_u16(65535)  # For inverted LED, high PWM = off
    else:
        led_pwm.duty_u16(0)      # For standard LED, low PWM = off

# AM312 motion detection with debouncing
def check_motion():
    raw_state = pir_sensor.value()
    
    # Simple debounce - take 3 readings
    if raw_state == 1:
        # Confirm with additional readings
        time.sleep(0.01)
        if pir_sensor.value() == 1:
            time.sleep(0.01)
            if pir_sensor.value() == 1:
                return True
    
    return False

# Cleanup function
def cleanup():
    led_off()
    print("Program stopped")

# Main loop
try:
    log_message("AM312 Motion Detection System Started")
    led_off()
    
    # Allow AM312 to stabilize
    log_message("Waiting 30 seconds for AM312 sensor to stabilize...")
    for i in range(30, 0, -10):
        log_message(f"Stabilization: {i} seconds remaining...")
        time.sleep(10)
    
    log_message("System ready! Monitoring for motion...")
    
    while True:
        current_time = get_timestamp()
        
        # Check for motion with debouncing
        if check_motion():
            # Motion detected
            last_motion_time = current_time
            
            # If LED is off, turn it on
            if not led_on:
                log_message("Motion detected - turning LED on")
                fade_in(led_pwm)
                led_on = True
        
        # If LED is on, check if it's time to turn it off
        if led_on and (current_time - last_motion_time > motion_timeout):
            log_message("Motion timeout - turning LED off")
            fade_out(led_pwm)
            led_on = False
        
        # Periodically log the sensor state (every 30 seconds)
        if int(current_time) % 30 == 0 and current_time - int(current_time) < 0.1:
            log_message(f"System status: Motion sensor active, LED is {'ON' if led_on else 'OFF'}")
        
        time.sleep(0.1)  # Short delay for loop execution

except KeyboardInterrupt:
    log_message("Keyboard interrupt detected")
except Exception as e:
    log_message(f"Error: {e}")
finally:
    cleanup()