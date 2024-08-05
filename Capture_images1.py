# Auto capture 10images from left camera and 10 images from right camera

import time
import os
from picamera2 import Picamera2

# Function to capture images from a specific camera
def capture_images(camera_index, folder, num_images, delay):
    # Ensure the directory exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Initialize the camera
    try:
        camera = Picamera2(camera_num=camera_index)
        camera.preview_configuration.main.size = (1640, 1232)
        camera.preview_configuration.main.format = "RGB888"
        camera.preview_configuration.align()
        camera.configure("preview")
        camera.start()
        
        for i in range(num_images):
            filename = os.path.join(folder, f"image_{i:02d}.jpg")
            print(f"Capturing {filename} from camera {camera_index}")
            camera.capture_file(filename)
            time.sleep(delay)
        
        camera.stop()
    except Exception as e:
        print(f"Failed to initialize camera {camera_index}: {e}")

# Define the folder paths
left_folder = '/home/lab902/Documents/Camera Calibration/NNL'
right_folder = '/home/lab902/Documents/Camera Calibration/NNR'

# Capture images from both cameras
num_images = 10
delay_between_captures = 1  # seconds

# Capture images from left camera
capture_images(camera_index=0, folder=left_folder, num_images=num_images, delay=delay_between_captures)
# Short delay to ensure proper release of resources
time.sleep(1)
# Capture images from right camera
capture_images(camera_index=1, folder=right_folder, num_images=num_images, delay=delay_between_captures)
