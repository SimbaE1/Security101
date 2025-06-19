from __future__ import print_function
# -*- coding: utf-8 -*-
import threading
import subprocess
import time
import tempfile
import os
# Your mobile number in E.164 format
YOUR_PHONE_NUMBER = "+1YOUR_PHONE_NUMBER"  # e.g., +1234567890

def call_me_via_facetime():
    """Kick off a FaceTime Audio call to your number."""
    subprocess.Popen(["open", f"facetime-audio://{YOUR_PHONE_NUMBER}"])

def send_imessage_with_images(images, msg):
    """
    Send an iMessage to yourself with attached images.
    `images` is a list of filepaths.
    """
    # Build AppleScript to send text and attachments
    attachments_cmd = ""
    for img in images:
        attachments_cmd += f' send POSIX file "{img}"\n'
    apple_script = f'''
    tell application "Messages"
      set targetService to 1st service whose service type = iMessage
      set targetBuddy to buddy "{YOUR_PHONE_NUMBER}" of targetService
      send "{msg}" to targetBuddy
      {attachments_cmd}
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script])

ALERT_REPEAT_INTERVAL = 30  # seconds between repeated alerts
last_alert_time = 0

def trigger_alarm():
    # play alarm sound once using macOS afplay
    subprocess.Popen(['afplay', 'alarm.mp3'])

ALERT_MESSAGE = (
    "Are you authorized to be in this room? "
    "A message has been sent to Ezra, with live feed. "
    "If you are supposed to be here, stay. "
    "If not, please leave. "
    "Put back all that has been put out of place. Thank you."
)
import re
import face_recognition
import sys
import numpy as np
import cv2


def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for person_name in os.listdir(known_people_folder):
        person_folder = os.path.join(known_people_folder, person_name)
        if not os.path.isdir(person_folder):
            continue
        for file in image_files_in_folder(person_folder):
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 1:
                print(f"WARNING: More than one face found in {file}. Deleting file.")
                os.remove(file)
                continue

            if len(encodings) == 0:
                print(f"WARNING: No faces found in {file}. Deleting file.")
                os.remove(file)
                continue

            # valid encoding found
            known_names.append(person_name)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings


def print_result(filename, name, distance, show_distance=False):
    if show_distance:
        print("{},{},{}".format(filename, name, distance))
    else:
        print("{},{}".format(filename, name))


def test_image(image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            [print_result(image_to_check, name, distance, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else:
            print_result(image_to_check, "unknown_person", None, show_distance)

    if not unknown_encodings:
        # print out fact that no faces were found in image
        print_result(image_to_check, "no_persons_found", None, show_distance)


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    # macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    )

    pool.starmap(test_image, function_parameters)


if __name__ == "__main__":
    # Continuous capture loop
    KNOWN_FACES_DIR = "known_people_folder"  # adjust as needed
    known_names, known_face_encodings = scan_known_people(KNOWN_FACES_DIR)
    print("Known people loaded:")
    for name in known_names:
        print(f" - {name}")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        sys.exit(1)
    print("Starting video stream. Press 'q' to quit.")
    unknown_present = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR to RGB for detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Detect faces and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if face_encodings:
            # Check all faces: any unknown?
            unknown = False
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                if True in matches:
                    name = known_names[matches.index(True)]
                    print(f"{name} detected")
                else:
                    unknown = True

            now = time.time()
            if unknown:
                # If first detection or interval elapsed, alert
                if not unknown_present or (now - last_alert_time) >= ALERT_REPEAT_INTERVAL:
                    print(ALERT_MESSAGE)
                    threading.Thread(target=trigger_alarm, daemon=True).start()
                    subprocess.Popen(['say', ALERT_MESSAGE])

                    # 1) Place the FaceTime Audio call
                    call_me_via_facetime()

                    # 2) Capture and send cropped images of each unknown face
                    cropped_paths = []
                    for i, loc in enumerate(face_locations):
                        matches = face_recognition.compare_faces([known_face_encodings[j] for j in range(len(known_face_encodings))], face_encodings[i], tolerance=0.6)
                        if True not in matches:
                            top, right, bottom, left = loc
                            crop = frame[top:bottom, left:right]
                            fd, path = tempfile.mkstemp(suffix=".jpg")
                            os.close(fd)
                            cv2.imwrite(path, crop)
                            cropped_paths.append(path)

                    send_imessage_with_images(cropped_paths, ALERT_MESSAGE)

                    unknown_present = True
                    last_alert_time = now
            else:
                # reset tracking when nobody unknown
                unknown_present = False
        # Display live feed
        cv2.imshow("Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()