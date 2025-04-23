# Motion-Sensing LED light

## Hardware Components
- **Raspberry Pi Pico 2W**
- **AM312 PIR Motion Sensor**
- **LED** LED 32mm 6251 1C8B (from a random desk lamp)
- **10K Resistor** (pull-down)

## Connections
- **Motion Sensor**
  - VCC → 3.3V on Pico
  - VOUT → GPIO 14 on Pico
  - GND → GND on Pico
  - *10K pull-down resistor between VOUT and GND*

- **LED**
  - Positive (+) → GPIO 13 on Pico
  - Negative (-) → GND on Pico

## Files
- `main.py`
- `pir_diagnostic.py` - Utility to verify sensor functionality

## Usage Guide
1. Upload `pir_diagnostic.py` to test sensor functionality
2. Upload `main.py` for normal operation
3. System will stabilize for 30 seconds, then begin monitoring
4. LED will fade in when motion is detected, fade out 10 seconds after motion stops