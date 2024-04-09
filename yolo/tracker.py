import os
import cv2
from ultralytics import YOLO

TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(TRACKER_DIR, 'videos')
video_name = 'vid5.mp4'

video_path = os.path.join(VIDEOS_DIR, video_name)
video_path_out = '{}_out.mp4'.format(video_path)

if not os.path.exists(video_path):
    print(f"Error: Video file '{video_path}' not found.")
    exit()

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()

H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join(TRACKER_DIR, 'model.pt')

model = YOLO(model_path)

threshold = 0.7

reference_object_width = 0.05  # Adjust based on your reference object

# Get frame rate
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Initialize variables for tracking
bullet_centroid_prev = None  # Store previous bullet centroid (x, y)

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        speed = 0

        if score > threshold:  # Only process if score above threshold
            # Calculate bullet centroid
            bullet_centroid = (int((x1 + x2) / 2), int((y1 + y2) / 2))

            # Calculate speed if previous centroid exists (i.e., tracking)
            if bullet_centroid_prev is not None:
                # Distance traveled in pixels between frames
                distance_pixels = ((bullet_centroid[0] - bullet_centroid_prev[0])**2 
                                  + (bullet_centroid[1] - bullet_centroid_prev[1])**2)**0.5

                # Convert pixel distance to real units based on reference object
                distance_real_units = distance_pixels * reference_object_width / (x2 - x1)  

                # Calculate speed (considering frame rate)
                speed = distance_real_units * frame_rate

            # Update previous centroid for next frame
            bullet_centroid_prev = bullet_centroid

            # Draw bounding box and label
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, f"{results.names[int(class_id)].upper()} {speed:.2f} m/s", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()
