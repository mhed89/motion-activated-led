# Motion-Sensing Smart Light System
### Powered by Raspberry Pi Pico 2W

## Overview
A compact motion-activated lighting solution that uses smooth fading effects for a natural lighting experience.
## Hardware Components
- **Raspberry Pi Pico 2W**
- **AM312 PIR Motion Sensor** - Detects human movement
- **LED** - LED 32mm 6251 1C8B (see image), should work with whatever LED..
- **10K Resistor** - Pull-down for reliable sensor operation

## Connections
- **Motion Sensor**
  - VCC → 3.3V on Pico
  - VOUT → GPIO 14 on Pico (with 10K pull-down to GND)
  - GND → GND on Pico

- **LED**
  - Positive (+) → GPIO 13 on Pico (with current-limiting resistor)
  - Negative (-) → GND on Pico

## Key Features
- **Instant Activation** - Lights up immediately when motion is detected
- **Natural Fading** - Gamma correction for smooth light transitions
- **Energy Efficient** - LED only active when needed
- **Quick Setup** - 5-second initialization, then fully automatic
- **Customizable** - Adjust timing and brightness in code

## Software Files
- `main.py` - Primary motion detection program (auto-runs on boot)
- `pir_diagnostic.py` - Tool to verify sensor functionality

## Quick Start Guide
1. Connect hardware components as specified
2. Upload `pir_diagnostic.py` to test sensor functionality
3. Upload `main.py` for normal operation
4. Power the Pico to begin monitoring

## Customization Options
- Modify `motion_timeout` in code to change how long LED stays on
- Adjust fade parameters for faster/slower transitions
- Set `inverted_led` value based on your LED connection type

---

**Project Creator:** mhed89  
**Date Created:** 2025-04-23

*A MicroPython-powered Smart Home Project*