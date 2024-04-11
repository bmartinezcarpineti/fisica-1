import os
import cv2
from ultralytics import YOLO

# files constants
TRACKER_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEOS_DIRECTORY = os.path.join(TRACKER_DIRECTORY, 'videos')
INPUT_VIDEO_NAME = 'vid6.mp4'
INPUT_VIDEO_PATH = os.path.join(INPUT_VIDEOS_DIRECTORY, INPUT_VIDEO_NAME)
OUTPUT_VIDEO_PATH = '{}_out.mp4'.format(INPUT_VIDEO_PATH)
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY, 'model.pt')

if not os.path.exists(INPUT_VIDEO_PATH):
    print(f"Error: Video file '{INPUT_VIDEO_PATH}' not found.")
    exit()

# video constants
OBJECT_WIDTH_IN_METERS = 0.05
OBJECT_WIDTH_IN_PIXELS = 110
PIXELS_PER_METER = OBJECT_WIDTH_IN_PIXELS / OBJECT_WIDTH_IN_METERS
ORIGINAL_INPUT_VIDEO_FPS = 120
TIME_DIFFERENCE = 1 / ORIGINAL_INPUT_VIDEO_FPS

# AI model constants
THRESHOLD_CONFIDENCE_SCORE = 0.7

# video variables initalization
yolo_model = YOLO(YOLO_MODEL_PATH)
input_video = cv2.VideoCapture(INPUT_VIDEO_PATH)
successful_video_reading, frame = input_video.read()
input_video_frame_height, input_video_frame_width, _ = frame.shape
output_video = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'MP4V'), int(input_video.get(cv2.CAP_PROP_FPS)), (input_video_frame_width, input_video_frame_height))

# object variables initalization
object_speed_in_x = 0
object_acceleration_in_x = 0
previous_object_position_in_x = None
previous_object_speed_in_x = None

# object detection loop
while successful_video_reading:

    model_detection_results = yolo_model(frame)[0]

    for result in model_detection_results.boxes.data.tolist():
        object_x1, object_y1, object_x2, object_y2, detection_confidence_score, object_class_id = result

        if detection_confidence_score > THRESHOLD_CONFIDENCE_SCORE:
            object_position_in_x = int((object_x1 + object_x2) / 2) # the position is represented by the center of the bounding box in the X axis

            if previous_object_position_in_x is not None:
                # speed calculation
                traveled_distance_in_pixels = object_position_in_x - previous_object_position_in_x
                traveled_distance_in_meters = traveled_distance_in_pixels / PIXELS_PER_METER
                object_speed_in_x = traveled_distance_in_meters / TIME_DIFFERENCE
            
            if previous_object_speed_in_x is not None:
                # acceleration calculation
                object_speed_in_x_difference = object_speed_in_x - previous_object_speed_in_x
                object_acceleration_in_x = object_speed_in_x_difference / TIME_DIFFERENCE

            # updates previous variables for next frame
            previous_object_position_in_x = object_position_in_x
            previous_object_speed_in_x = object_speed_in_x

            # draws bounding box and label
            cv2.rectangle(frame, (int(object_x1), int(object_y1)), (int(object_x2), int(object_y2)), (0, 255, 0), 4)
            cv2.putText(frame, f"{object_speed_in_x:.2f} m/s {object_acceleration_in_x:.2f} m/s^2", 
                        (int(object_x1), int(object_y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 
                        (0, 255, 0), 3, cv2.LINE_AA)

    output_video.write(frame)
    successful_video_reading, frame = input_video.read() # gets next frame

# clean up
input_video.release()
output_video.release()
cv2.destroyAllWindows()
