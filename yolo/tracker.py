import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from ultralytics import YOLO

# files constants
TRACKER_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEOS_DIRECTORY_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'videos2')
INPUT_VIDEO_NAME = 'vid3-2.mp4'
INPUT_VIDEO_PATH = os.path.join(INPUT_VIDEOS_DIRECTORY_PATH, INPUT_VIDEO_NAME)
OUTPUT_VIDEO_PATH = '{}_out.mp4'.format(INPUT_VIDEO_PATH)
PLOTS_FILE_DIRECTORY = os.path.join(TRACKER_DIRECTORY_PATH, 'plots')
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'model.pt')

if not os.path.exists(INPUT_VIDEO_PATH):
    print(f"Error: Video file '{INPUT_VIDEO_PATH}' not found.")
    exit()

# video constants
OBJECT_WIDTH_IN_METERS = 0.05
OBJECT_WIDTH_IN_PIXELS = 96
PIXELS_PER_METER = OBJECT_WIDTH_IN_PIXELS / OBJECT_WIDTH_IN_METERS
ORIGINAL_INPUT_VIDEO_FPS = 240
TIME_DIFFERENCE = 1 / ORIGINAL_INPUT_VIDEO_FPS # unit: seconds

# AI model constants
THRESHOLD_CONFIDENCE_SCORE = 0.7

# video variables initalization
yolo_model = YOLO(YOLO_MODEL_PATH)
input_video = cv2.VideoCapture(INPUT_VIDEO_PATH)
successful_video_reading, frame = input_video.read()
input_video_frame_height, input_video_frame_width, _ = frame.shape
output_video = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'MP4V'), int(input_video.get(cv2.CAP_PROP_FPS)), (input_video_frame_width, input_video_frame_height))

# object variables and constants initalization
current_time = 0
object_speed_in_x = 0
object_acceleration_in_x = 0
previous_object_position_in_x = None
previous_object_speed_in_x = None
all_object_position_in_x = []
all_object_speed_in_x = []
all_object_acceleration_in_x = []
all_object_force_in_x = []
all_object_detection_time = []
OBJECT_MASS = 0.283 # unit: kg
GRAVITY = 9.81

# object detection loop
while successful_video_reading:

    model_detection_results = yolo_model(frame)[0]
    current_time += TIME_DIFFERENCE

    for result in model_detection_results.boxes.data.tolist():
        object_x1, object_y1, object_x2, object_y2, detection_confidence_score, object_class_id = result

        if detection_confidence_score > THRESHOLD_CONFIDENCE_SCORE:
            all_object_detection_time.append(current_time)
            object_position_in_x = int((object_x1 + object_x2) / 2) # the position is represented by the center of the bounding box in the X axis
            all_object_position_in_x.append(object_position_in_x / PIXELS_PER_METER)

            if previous_object_position_in_x is not None:
                # speed calculation
                traveled_distance_in_pixels = object_position_in_x - previous_object_position_in_x
                traveled_distance_in_meters = traveled_distance_in_pixels / PIXELS_PER_METER
                object_speed_in_x = traveled_distance_in_meters / TIME_DIFFERENCE
                all_object_speed_in_x.append(object_speed_in_x)
            
            if previous_object_speed_in_x is not None:
                # acceleration calculation
                object_speed_in_x_difference = object_speed_in_x - previous_object_speed_in_x
                object_acceleration_in_x = object_speed_in_x_difference / TIME_DIFFERENCE
                all_object_acceleration_in_x.append(object_acceleration_in_x)

            # updates previous variables for next frame
            previous_object_position_in_x = object_position_in_x
            previous_object_speed_in_x = object_speed_in_x

            # draws bounding box and label
            cv2.rectangle(frame, (int(object_x1), int(object_y1)), (int(object_x2), int(object_y2)), (0, 255, 0), 4)
            cv2.putText(frame, f"{(object_position_in_x / PIXELS_PER_METER):.2f} m, {object_speed_in_x:.2f} m/s, {object_acceleration_in_x:.2f} m/s^2", 
                        (int(object_x1), int(object_y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    output_video.write(frame)
    successful_video_reading, frame = input_video.read() # gets next frame

# clean up
input_video.release()
output_video.release()
cv2.destroyAllWindows()


# dynamic friction coefficient calculation

dynamic_friction_coefficient = - (sum(all_object_acceleration_in_x)/len(all_object_acceleration_in_x)) / GRAVITY # ud = -a/g

print(f"\n\nDynamic friction coefficient: {dynamic_friction_coefficient}\n\n")

# data interpolation
time_points_for_interpolated_plot = np.linspace(min(all_object_detection_time), max(all_object_detection_time), 100)

object_position_interpolation = interp1d(all_object_detection_time, all_object_position_in_x, kind='linear')
all_object_interpolated_position_in_x = object_position_interpolation(time_points_for_interpolated_plot)

all_object_speed_in_x.insert(0,0)
object_speed_interpolation = interp1d(all_object_detection_time, all_object_speed_in_x, kind='cubic')
all_object_interpolated_speed_in_x = object_speed_interpolation(time_points_for_interpolated_plot)

all_object_acceleration_in_x.insert(0,0)
object_acceleration_interpolation = interp1d(all_object_detection_time, all_object_acceleration_in_x, kind='cubic')
all_object_interpolated_acceleration_in_x = object_acceleration_interpolation(time_points_for_interpolated_plot)

# object variables in function of time plot
plt.subplot(311)
plt.plot(time_points_for_interpolated_plot, all_object_interpolated_position_in_x, label="Position in X")
plt.ylabel("m")
plt.legend()

plt.subplot(312)
plt.plot(time_points_for_interpolated_plot, all_object_interpolated_speed_in_x, label="Speed in X")
plt.ylabel("m/s")
plt.legend()

plt.subplot(313)
plt.plot(time_points_for_interpolated_plot, all_object_interpolated_acceleration_in_x, label="Acceleration in X")
plt.ylabel("m/s^2")
plt.xlabel("Time (s)")
plt.legend()

plt.savefig(os.path.join(PLOTS_FILE_DIRECTORY, 'object_in_function_of_time.png'))

plt.clf()

# force in function of position calculation
for acceleration in all_object_acceleration_in_x:
    all_object_force_in_x.append(OBJECT_MASS * acceleration)
''' 
# data interpolation
#position_in_x_points_for_interpolated_plot = np.linspace(min(all_object_position_in_x), max(all_object_position_in_x), 100)

object_acceleration_position_interpolation = interp1d(all_object_position_in_x, all_object_acceleration_in_x, kind='cubic')
all_object_interpolated_acceleration_position = object_acceleration_position_interpolation(position_in_x_points_for_interpolated_plot)

object_force_position_interpolation = interp1d(all_object_position_in_x, all_object_force_in_x, kind='cubic')
all_object_interpolated_force_position = object_force_position_interpolation(position_in_x_points_for_interpolated_plot)

# object variables in function of position plot
plt.subplot(211)
plt.plot(position_in_x_points_for_interpolated_plot, all_object_interpolated_acceleration_position, label="Acceleration in X")
plt.ylabel("m/s^2")
plt.legend()

plt.subplot(212)
plt.plot(position_in_x_points_for_interpolated_plot, all_object_interpolated_force_position, label="Force in X")
plt.ylabel("N (kg * m/s^2)")
plt.xlabel("Position in X (m)")
plt.legend()

plt.savefig(os.path.join(PLOTS_FILE_DIRECTORY, 'object_in_function_of_position.png'))
'''