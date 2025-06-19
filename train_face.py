#!/usr/bin/env python3
import cv2
import os
import argparse
import re

def capture_faces(output_folder, name_prefix, count=10):
    os.makedirs(output_folder, exist_ok=True)
    person_folder = os.path.join(output_folder, name_prefix)
    os.makedirs(person_folder, exist_ok=True)
    # Determine starting index based on existing images
    existing_files = [f for f in os.listdir(person_folder) if re.match(r'imgs_\d+\.jpg', f)]
    start_index = len(existing_files)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    print(f"Capturing {count} face images. Press 'q' to quit early.")
    captured = 0
    while captured < count:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Capture Face - Press 'c' to capture", frame)
        key = cv2.waitKey(1) & 0xFF
        # Press 'c' to capture current frame
        if key == ord('c'):
            index = start_index + captured + 1
            filename = os.path.join(person_folder, f"imgs_{index}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured {filename}")
            captured += 1
        elif key == ord('q'):
            print("Capture aborted by user.")
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Training data capture complete.")

def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []
    for person_name in os.listdir(known_people_folder):
        person_dir = os.path.join(known_people_folder, person_name)
        if not os.path.isdir(person_dir):
            continue
        for img_path in image_files_in_folder(person_dir):
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 1:
                click.echo(f"WARNING: More than one face found in {img_path}. Only considering the first face.")
            if len(encodings) == 0:
                click.echo(f"WARNING: No faces found in {img_path}. Ignoring file.")
            else:
                known_names.append(person_name)
                known_face_encodings.append(encodings[0])
    return known_names, known_face_encodings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture face images for training")
    parser.add_argument("--output", default="known_people_folder", help="Folder to save captured images")
    parser.add_argument("--name", required=True, help="Prefix name for saved images")
    parser.add_argument("--count", type=int, default=10, help="Number of images to capture")
    args = parser.parse_args()

    # Print existing known people
    existing = [d for d in os.listdir(args.output) if os.path.isdir(os.path.join(args.output, d))]
    if existing:
        print("Existing known people:")
        for name in existing:
            print(f" - {name}")
    else:
        print("No known people found yet.")

    capture_faces(args.output, args.name, args.count)