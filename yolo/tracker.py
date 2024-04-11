import os
import cv2
from ultralytics import YOLO

#Files constants
TRACKER_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIRECTORY = os.path.join(TRACKER_DIRECTORY, 'videos')
INPUT_VIDEO_PATH = os.path.join(VIDEOS_DIRECTORY, 'vid6.mp4')
OUTPUT_VIDEO_PATH = '{}_out.mp4'.format(INPUT_VIDEO_PATH)
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY, 'model.pt')

if not os.path.exists(INPUT_VIDEO_PATH):
    print(f"Error: Video file '{INPUT_VIDEO_PATH}' not found.")
    exit()

#Video and AI constants
THRESHOLD_CONFIDENCE_SCORE = 0.7
OBJECT_WIDTH_IN_METERS = 0.05
ORIGINAL_INPUT_VIDEO_FPS = 120
TIME_DIFFERENCE = 1 / ORIGINAL_INPUT_VIDEO_FPS

yolo_model = YOLO(YOLO_MODEL_PATH)
input_video = cv2.VideoCapture(INPUT_VIDEO_PATH)
successful_video_reading, frame = input_video.read()
input_video_frame_height, input_video_frame_width, _ = frame.shape
output_video = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'MP4V'), int(input_video.get(cv2.CAP_PROP_FPS)), (input_video_frame_width, input_video_frame_height))

# Initialize variables for tracking
object_centroid_prev = None  # Store previous bullet centroid (x, y)
object_speed_prev = None

while successful_video_reading:

    results = yolo_model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        object_speed = 0
        object_acceleration = 0

        if score > THRESHOLD_CONFIDENCE_SCORE:  # Only process if score above threshold
            # Calculate bullet centroid
            object_centroid = (int((x1 + x2) / 2), int((y1 + y2) / 2))

            # Calculate speed if previous centroid exists (i.e., tracking)
            if object_centroid_prev is not None:
                # Distance traveled in pixels between frames
                distance_pixels = ((object_centroid[0] - object_centroid_prev[0])**2 
                                  + (object_centroid[1] - object_centroid_prev[1])**2)**0.5

                # Convert pixel distance to real units based on reference object
                pixels_per_meter = (x2 - x1) / OBJECT_WIDTH_IN_METERS

                distance_real_units = distance_pixels / pixels_per_meter

                # Calculate speed (considering frame rate)
                
                object_speed = distance_real_units / TIME_DIFFERENCE
            
            if object_speed_prev is not None:
                
                object_acceleration = (object_speed - object_speed_prev) / TIME_DIFFERENCE

            # Update previous centroid for next frame
            object_centroid_prev = object_centroid

            object_speed_prev = object_speed

            # Draw bounding box and label
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, f"{object_speed:.2f} m/s {object_acceleration:.2f} m/s^2", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    output_video.write(frame)
    successful_video_reading, frame = input_video.read()

input_video.release()
output_video.release()
cv2.destroyAllWindows()
