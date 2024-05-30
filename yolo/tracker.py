import os
import cv2
import csv
from ultralytics import YOLO

# files constants
TRACKER_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEOS_DIRECTORY_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'videos3')
INPUT_VIDEO_NAME = 'tarro3.mp4'
INPUT_VIDEO_PATH = os.path.join(INPUT_VIDEOS_DIRECTORY_PATH, INPUT_VIDEO_NAME)
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'model.pt')
OUTPUT_CSV_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'data/positions.csv')

if not os.path.exists(INPUT_VIDEO_PATH):
    print(f"Error: Video file '{INPUT_VIDEO_PATH}' not found.")
    exit()

# video constants
OBJECT_WIDTH_IN_METERS = 0.055
OBJECT_WIDTH_IN_PIXELS = 165
PIXELS_PER_METER = OBJECT_WIDTH_IN_PIXELS / OBJECT_WIDTH_IN_METERS
ORIGINAL_INPUT_VIDEO_FPS = 240
TIME_DIFFERENCE = 1 / ORIGINAL_INPUT_VIDEO_FPS # unit: seconds

# AI model constants
THRESHOLD_CONFIDENCE_SCORE = 0.7

# video variables initalization
yolo_model = YOLO(YOLO_MODEL_PATH)
input_video = cv2.VideoCapture(INPUT_VIDEO_PATH)
successful_video_reading, frame = input_video.read()

# object variables and constants initalization
current_time = 0
all_object_detection_time = []
all_object_position_in_x = []

# object detection loop
while successful_video_reading:

    model_detection_results = yolo_model(frame)[0]
    current_time += TIME_DIFFERENCE

    for result in model_detection_results.boxes.data.tolist():
        object_x1, object_y1, object_x2, object_y2, detection_confidence_score, object_class_id = result

        if detection_confidence_score > THRESHOLD_CONFIDENCE_SCORE:
            all_object_detection_time.append(current_time)
            position = int((object_x1 + object_x2) / 2) # the position is represented by the center of the bounding box in the X axis
            all_object_position_in_x.append(position / PIXELS_PER_METER)

    successful_video_reading, frame = input_video.read() # gets next frame

# clean up
input_video.release()
cv2.destroyAllWindows()

# saves results to csv
with open(OUTPUT_CSV_PATH, 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["time","position"])
    for time,position in zip(all_object_detection_time,all_object_position_in_x):
        writer.writerow([time,position])