import os
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

# files constants
TRACKER_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEOS_DIRECTORY = os.path.join(TRACKER_DIRECTORY, 'videos')
INPUT_VIDEO_NAME = 'vid8.mp4'
INPUT_VIDEO_PATH = os.path.join(INPUT_VIDEOS_DIRECTORY, INPUT_VIDEO_NAME)
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY, 'model.pt')

if not os.path.exists(INPUT_VIDEO_PATH):
    print(f"Error: Video file '{INPUT_VIDEO_PATH}' not found.")
    exit()

# AI model constants
THRESHOLD_CONFIDENCE_SCORE = 0.7

# video variables initalization
yolo_model = YOLO(YOLO_MODEL_PATH)
input_video = cv2.VideoCapture(INPUT_VIDEO_PATH)
successful_video_reading, frame = input_video.read()
object_width_in_pixels_sumatory = 0
object_detection_counter = 0
all_object_width_in_pixels = []

# object detection loop
while successful_video_reading:

    model_detection_results = yolo_model(frame)[0]

    for result in model_detection_results.boxes.data.tolist():
        object_x1, object_y1, object_x2, object_y2, detection_confidence_score, object_class_id = result

        if detection_confidence_score > THRESHOLD_CONFIDENCE_SCORE:
            object_detection_counter+=1
            object_width_in_pixels_sumatory+=(object_x2-object_x1)
            all_object_width_in_pixels.append(object_x2-object_x1)

    successful_video_reading, frame = input_video.read() # gets next frame

# clean up
input_video.release()
cv2.destroyAllWindows()

print(f"\nThe average width in pixels of the object in this video is: \
{object_width_in_pixels_sumatory / object_detection_counter}\n\
All detected width of the object are: {all_object_width_in_pixels}\n")