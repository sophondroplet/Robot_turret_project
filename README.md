# Robot Turret Project

This repository contains the firmware and a Python-based desktop control application for a small robot turret. The Arduino sketch drives multiple servos and motors; the Python app provides a GUI for camera preview, aiming controls and serial communication to the turret.

Summary
- Arduino firmware: `Software/Arduino firmware/Turret.ino`
- Python control app: `Software/Python_app/` (PyQt6 GUI, OpenCV camera preview, serial comms)

Quick overview
- The Python GUI captures camera frames via OpenCV and shows them in a PyQt6 window. The user aims the turret using an on-screen control box and keyboard/mouse. The GUI constructs a compact command string and sends it over serial to the Arduino.
- The Arduino receives commands, parses X/Y/Z servo positions, motor flags (fast/slow) and reload trigger, and moves servos / toggles motor outputs accordingly.

Hardware / wiring notes
- The Arduino pins used by the sketch (`Turret.ino`):
  - SERVO_X -> pin 7
  - SERVO_Y1 -> pin 8
  - SERVO_Y2 -> pin 6 (mirrored)
  - SERVO_Z -> pin 9
  - FAST_MOTORS -> pin 11 (digital output)
  - SLOW_MOTOR -> pin 3 (digital output / PWM)
- The sketch expects standard hobby servos and separate power supply for motors/servos as needed. Do not power multiple servos from the Arduino 5V regulator if they draw significant current; use an external 5V supply and common ground.

Software requirements
- Tested on Windows with Python 3.8+ (3.10 recommended).
- Python dependencies (also included in `Software/Python_app/requirements.txt`):
  - pyqt6
  - opencv-python
  - pyserial
  - mouse
  - numpy

Setup (Windows - PowerShell)
1. Install Python 3.8+ from python.org and ensure `python` is on your PATH.
2. Open PowerShell and create a virtual environment inside the Python app folder (recommended):

```powershell
cd .\Software\Python_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r .\requirements.txt
```

3. Install Arduino IDE (or use `arduino-cli`) to upload firmware.

Upload firmware to Arduino
1. Open `Software/Arduino firmware/Turret.ino` in the Arduino IDE.
2. Select the correct board and COM port.
3. Verify and upload.

Run the Python control app
1. With the virtual environment activated (see above), run:

```powershell
cd .\Software\Python_app
python main.py
```

2. The app starts with a settings screen. Choose:
  - Camera index (0,1,2... depending on your camera)
  - Resolution: 640x480, 1280x720 or 1920x1080 (your camera must support the chosen resolution)
  - Serial port: the COM port the Arduino is on (e.g., COM3)
  - Click Start

3. The app will attempt to open the camera and establish a serial handshake with the Arduino. The Arduino firmware sends a handshake character 'C' while waiting for the GUI; the GUI waits for that before proceeding.

How the communication format works
- The Python app sends a single-line command every frame (60Hz target):

  X{X}Y{Y}Z{Z}S{S}F{F}R{R}\n

  - X: integer 0–180 (pan servo)
  - Y: integer 0–125 (tilt servo)
  - Z: integer 0–120 (elevation / other servo)
  - S: 0 or 1 (slow motor flag)
  - F: 0 or 1 (fast motor flag)
  - R: 0 or 1 (reload trigger)

Example line the app sends:

  X90Y80Z100S0F1R0\n

On the Arduino side, `Turret.ino` uses parsing functions (parseX, parseY, parseZ, parseS, parseF, parseR) to extract values from the incoming string and then updates servo outputs and motor digital pins accordingly.

Controls (GUI)
- Mouse: move inside the on-screen ControlBox to change X/Y (pan/tilt).
- Right mouse button = charge; left click while charged = shoot. The app maps these to `charge` and `shoot` boolean flags sent in the command string.
- Keyboard: W/S increase/decrease Z (elevation) while pressed. R toggles reload_mode (sends R flag when active). Escape stops camera and returns to settings.

Troubleshooting
- Camera fails to open: ensure the camera index is correct and no other program is holding the camera. Try lower resolution.
- Serial errors / no COM ports shown: verify Arduino is connected and drivers installed. Use Device Manager to confirm the COM port. Close any other applications that may be using the port.
- Permissions: on Windows, PowerShell with normal privileges is usually OK. If you experience permission errors, try running PowerShell as Administrator temporarily.

Developer notes (code map)
- `Software/Arduino firmware/Turret.ino` — Arduino sketch: servo and motor control logic and serial parsing.
- `Software/Python_app/main.py` — application entrypoint and main timer loop.
- `Software/Python_app/main_window.py` — main PyQt window, orchestrates camera, UI and serial manager.
- `Software/Python_app/camera.py` — OpenCV camera wrapper and conversion to Qt image.
- `Software/Python_app/settings_menu.py` — initial settings UI to choose camera/resolution/COM port.
- `Software/Python_app/controls.py` — top-level controls widget and state for X/Y/Z.
- `Software/Python_app/control_box.py` — interactive aiming widget (mouse + keyboard handling).
- `Software/Python_app/serial_manager.py` — pyserial wrapper: open/close, handshake and write commands.
- `Software/Python_app/turretvsc.py` — currently empty (placeholder)

Safety
- This project may move motors and servos. Remove loose objects, secure the turret, and do a dry-run without projectiles or moving parts connected to the motors. Use proper power supply ratings and fusing where appropriate.

Next steps / suggestions
- Add a small CLI or tray icon for starting/stopping the app.
- Add calibration UI to map on-screen positions to real turret angles.
- Add unit tests and a small smoke-test script that simulates Arduino responses for development without hardware.

License
- No license file included. Add one if you intend to make the project public.

Contact
- For questions about the code layout, open an issue or contact the project owner.
