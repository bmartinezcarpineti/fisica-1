import os
import cv2
from ultralytics import YOLO

TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(TRACKER_DIR, 'videos')
video_name = 'vid6.mp4'

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

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold: 
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()