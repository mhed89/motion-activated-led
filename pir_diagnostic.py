from machine import Pin
import time

# Setup for AM312 PIR sensor
pir_pin = 14  # Current GPIO pin
pir_sensor = Pin(pir_pin, Pin.IN)

# Function to get timestamp
def get_timestamp():
    return time.time()

print(f"===== AM312 PIR SENSOR DIAGNOSTIC =====")
print(f"Starting diagnostic at {get_timestamp()}")

# First, let the sensor stabilize
print("Waiting 60 seconds for AM312 to stabilize...")
start_time = get_timestamp()
while get_timestamp() - start_time < 60:
    remaining = 60 - int(get_timestamp() - start_time)
    if remaining % 10 == 0 and remaining > 0:
        print(f"{remaining} seconds remaining for stabilization...")
    time.sleep(1)

print("\nBeginning AM312 test sequence...")
print("Stand still for 10 seconds, then move in front of sensor when prompted.")

# Check baseline with no movement
print("\n--- BASELINE TEST (No Movement) ---")
print("Please remain still for 10 seconds...")
time.sleep(3)

baseline_readings = []
start_time = get_timestamp()
while get_timestamp() - start_time < 10:
    reading = pir_sensor.value()
    baseline_readings.append(reading)
    time.sleep(0.5)

high_count = baseline_readings.count(1)
low_count = baseline_readings.count(0)
print(f"Baseline results: {high_count} HIGH, {low_count} LOW readings")

# Now test with movement
print("\n--- MOVEMENT TEST ---")
print("Please move in front of the sensor for 10 seconds...")
time.sleep(3)

movement_readings = []
start_time = get_timestamp()
while get_timestamp() - start_time < 10:
    reading = pir_sensor.value()
    movement_readings.append(reading)
    time.sleep(0.5)

high_count = movement_readings.count(1)
low_count = movement_readings.count(0)
print(f"Movement results: {high_count} HIGH, {low_count} LOW readings")

# Now test the recovery time
print("\n--- RECOVERY TEST ---")
print("Please remain still for 10 seconds...")
time.sleep(3)

recovery_readings = []
start_time = get_timestamp()
while get_timestamp() - start_time < 10:
    reading = pir_sensor.value()
    recovery_readings.append(reading)
    time.sleep(0.5)

high_count = recovery_readings.count(1)
low_count = recovery_readings.count(0)
print(f"Recovery results: {high_count} HIGH, {low_count} LOW readings")

# Analyze results
print("\n===== ANALYSIS =====")

if sum(baseline_readings) == len(baseline_readings):
    print("ISSUE: Sensor is STUCK HIGH during baseline (no movement)")
elif sum(baseline_readings) == 0:
    print("GOOD: Sensor correctly reads LOW when no movement")
else:
    print(f"WARNING: Mixed readings during baseline: {baseline_readings}")

if sum(movement_readings) > 0:
    print("GOOD: Sensor detected movement during movement test")
else:
    print("ISSUE: Sensor failed to detect any movement")

if sum(recovery_readings) < len(recovery_readings):
    print("GOOD: Sensor returned to LOW state after movement stopped")
else:
    print("ISSUE: Sensor remained HIGH after movement stopped")

# Final diagnosis
print("\n===== DIAGNOSIS =====")

if sum(baseline_readings) == len(baseline_readings) and sum(recovery_readings) == len(recovery_readings):
    print("The AM312 sensor appears to be STUCK in HIGH state.")
    print("Recommendations:")
    print("1. Check wiring - ensure proper GND connection")
    print("2. Try a different GPIO pin (with internal pull-down if possible)")
    print("3. Check for interference (heat sources, vibration, RF)")
    print("4. Ensure proper voltage (2.7V-12V, ideally 3.3V)")
    print("5. Try a different AM312 sensor")
elif sum(movement_readings) == 0:
    print("The AM312 sensor is NOT DETECTING motion.")
    print("Recommendations:")
    print("1. Check wiring - ensure power is connected")
    print("2. Check sensor orientation (lens should face detection area)")
    print("3. Try moving closer to the sensor")
    print("4. Check for physical obstructions on the lens")
    print("5. Try a different AM312 sensor")
else:
    print("The AM312 sensor appears to be WORKING as expected.")
    print("Recommendations for implementation:")
    print("1. Use appropriate stabilization time (60 seconds)")
    print("2. Implement debouncing in your motion detection code")
    print("3. Account for the 2-3 second fixed delay after motion stops")