# Security101: Mac Surveillance System

**Security101** is a Python-based face-recognition surveillance tool for macOS. It monitors a specified camera feed, detects unauthorized people, and sends real-time alerts via FaceTime Audio calls and iMessage with images.

## Features
- Continuous face recognition using the `face_recognition` library
- Automated image capture of unidentified or unauthorized individuals
- Real-time FaceTime Audio call alerts (requires Apple Developer setup)
- Real-time iMessage alerts with attached images
- Ignoring non-face images and handling files with multiple faces
- Extensible architecture for custom notification channels

## Requirements
- macOS 10.14+ with webcam support
- Python 3.8 or higher
- Homebrew (for installing dependencies)
- An Apple Developer account for FaceTime Audio (optional)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/security101.git
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
4. **Install system dependencies via Homebrew:**
   ```bash
   brew install ffmpeg
   ```

## Configuration

1. **Copy the example config:**
   ```bash
   cp config.example.yaml config.yaml
   ```
2. **Edit `config.yaml`** and set:
   - `camera_index`: Index of the webcam (usually `0`)
   - `authorized_faces_dir`: Directory path with images of authorized individuals
   - `your_phone_number`: Your mobile number in E.164 format for FaceTime and iMessage

## Usage

Run the main surveillance script:
```bash
python surveillance.py
```
- The script will log detections to `logs/` and save captured images to `captures/`.
- Unauthorized faces trigger a FaceTime Audio call and an iMessage containing captured images automatically.

## Adding Images to Existing Faces
- If a detected face matches an existing person, new images are added to their folder instead of overwriting.
- Ignored files (no faces or multiple faces) are removed automatically to keep the dataset clean.

## Custom Notifications

To add new notification channels, extend the `notifiers/` module:
1. Create a new notifier class inheriting from `BaseNotifier`.
2. Implement `send_alert(image_path: str, message: str)`.
3. Register your notifier in `config.yaml`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
