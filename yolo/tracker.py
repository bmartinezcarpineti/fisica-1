import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from ultralytics import YOLO
from scipy.signal import savgol_filter

# files constants
TRACKER_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEOS_DIRECTORY_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'videos3')
INPUT_VIDEO_NAME = 'tarro2.mp4'
INPUT_VIDEO_PATH = os.path.join(INPUT_VIDEOS_DIRECTORY_PATH, INPUT_VIDEO_NAME)
OUTPUT_VIDEO_PATH = '{}_out.mp4'.format(INPUT_VIDEO_PATH)
PLOTS_FILE_DIRECTORY = os.path.join(TRACKER_DIRECTORY_PATH, 'plots')
YOLO_MODEL_PATH = os.path.join(TRACKER_DIRECTORY_PATH, 'model.pt')

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
input_video_frame_height, input_video_frame_width, _ = frame.shape
output_video = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'MP4V'), int(input_video.get(cv2.CAP_PROP_FPS)), (input_video_frame_width, input_video_frame_height))

# object variables and constants initalization
current_time = 0
object_speed_in_x = 0
object_acceleration_in_x = 0
previous_position = None
previous_speed = None
previous_object_speed_in_x = None
all_object_position_in_x = []
all_object_distance_to_zero_in_x = []
all_object_speed_in_x = []
all_object_acceleration_in_x = []
all_object_force_in_x = []
all_object_detection_time = []
OBJECT_MASS = 0.283 # unit: kg
GRAVITY = 9.81
SPRING_L0 = 0.00135 # unit: mts
spring_l1 = 0

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

            # draws bounding box and label
            cv2.rectangle(frame, (int(object_x1), int(object_y1)), (int(object_x2), int(object_y2)), (0, 255, 0), 4)

    output_video.write(frame)
    successful_video_reading, frame = input_video.read() # gets next frame

all_object_position_in_x = all_object_position_in_x[::5]
all_object_detection_time = all_object_detection_time[::5]
#all_object_position_in_x = savgol_filter(all_object_position_in_x, 6, 2)

for position in all_object_position_in_x:
    if previous_position is not None:
        traveled_distance_in_pixels = position - previous_position
        traveled_distance_in_meters = traveled_distance_in_pixels / PIXELS_PER_METER
        object_speed_in_x = traveled_distance_in_meters / TIME_DIFFERENCE
        all_object_speed_in_x.append(object_speed_in_x)
    previous_position = position

#all_object_speed_in_x = savgol_filter(all_object_speed_in_x, 7, 2)

for speed in all_object_speed_in_x:
    if previous_speed is not None:
        object_speed_in_x_difference = speed - previous_speed
        object_acceleration_in_x = object_speed_in_x_difference / TIME_DIFFERENCE
        all_object_acceleration_in_x.append(object_acceleration_in_x)
    previous_speed = speed

#all_object_acceleration_in_x = savgol_filter(all_object_acceleration_in_x, 7, 2)

# clean up
input_video.release()
output_video.release()
cv2.destroyAllWindows()

# dynamic friction coefficient calculation
'''
dynamic_friction_coefficient = - (sum(all_object_acceleration_in_x)/len(all_object_acceleration_in_x)) / GRAVITY # ud = -a/g

print(f"\n\nDynamic friction coefficient: {dynamic_friction_coefficient}\n\n")
'''
# 

spring_zero_position = previous_position
all_object_distance_to_spring_zero_in_x = list(map(lambda x: x - spring_zero_position, all_object_position_in_x))
'''
# data interpolation
time_points_for_interpolated_plot = np.linspace(min(all_object_detection_time), max(all_object_detection_time), 50)

object_position_interpolation = interp1d(all_object_detection_time, all_object_position_in_x, kind='linear')
all_object_interpolated_position_in_x = object_position_interpolation(time_points_for_interpolated_plot)

#all_object_speed_in_x.insert(0,0)
all_object_detection_time.pop(0)
object_speed_interpolation = interp1d(all_object_detection_time, all_object_speed_in_x, kind='cubic')
all_object_interpolated_speed_in_x = object_speed_interpolation(time_points_for_interpolated_plot)

#all_object_acceleration_in_x.insert(0,0)
#all_object_acceleration_in_x.insert(0,0)
all_object_detection_time.pop(0)
object_acceleration_interpolation = interp1d(all_object_detection_time, all_object_acceleration_in_x, kind='cubic')
all_object_interpolated_acceleration_in_x = object_acceleration_interpolation(time_points_for_interpolated_plot)
'''
# object variables in function of time plot
plt.subplot(311)
#plt.plot(time_points_for_interpolated_plot, all_object_interpolated_position_in_x, label="Position in X")
plt.plot(all_object_detection_time, all_object_position_in_x, label="Position in X")
plt.ylabel("m")
plt.legend()

plt.subplot(312)
#plt.plot(time_points_for_interpolated_plot, all_object_interpolated_speed_in_x, label="Speed in X")
all_object_detection_time.pop(0)
plt.plot(all_object_detection_time, all_object_speed_in_x, label="Speed in X")
plt.ylabel("m/s")
plt.legend()

plt.subplot(313)
#plt.plot(time_points_for_interpolated_plot, all_object_interpolated_acceleration_in_x, label="Acceleration in X")
all_object_detection_time.pop(0)
plt.plot(all_object_detection_time, all_object_acceleration_in_x, label="Acceleration in X")
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