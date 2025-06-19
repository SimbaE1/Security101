# Security101: Mac Surveillance System

**Security101** monitors a webcam on macOS, detects unauthorized people in real time, and immediately alerts you via FaceTime Audio calls and iMessage with snapshots.

## Features
- Continuous face detection and recognition using the `face_recognition` library
- Automatic removal of images with no or multiple faces
- Real-time FaceTime Audio call alerts when an unknown face is detected
- Real-time iMessage alerts with captured face images
- Easy training data capture for adding new known faces

## Requirements
- macOS 10.14 or later with a functional webcam
- Python 3.8 or newer
- Installed Python dependencies: `face_recognition`, `opencv-python`
- Your Mac signed into your Apple ID for Messages and FaceTime
- Camera & screen‑recording permissions granted in System Settings


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SimbaE1/security101.git
   cd security101
   ```
2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install system dependencies via Homebrew (for camera and audio tools):**
   ```bash
   brew install ffmpeg
   ```

## Commands
- `python recognition.py`
  - Launches the surveillance loop: opens the webcam, performs face recognition, and issues alerts.
- `python recognition.py --help`
  - Displays available options for the surveillance script (e.g., customizing tolerance or camera index).
- `python capture_faces.py --name <PersonName> --count <N>`
  - Opens a capture window; press **c** to save up to N images for the specified person under `known_people_folder/PersonName/`.
- `python capture_faces.py --help`
  - Shows usage details and options for the capture script.

## Notes
- Ensure you set `YOUR_PHONE_NUMBER` in `recognition.py` to your mobile number in E.164 format.
- For clear recognition results, provide good-quality, well-lit face images when capturing training data.
- If you need to adjust detection sensitivity or camera device, use the `--help` flags to customize parameters.
