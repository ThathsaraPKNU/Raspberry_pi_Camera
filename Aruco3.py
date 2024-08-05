#detect the marker

import cv2
import cv2.aruco as aruco
import numpy as np
from picamera2 import Picamera2

# Define ArUco dictionary and parameters
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
PARAMETERS = aruco.DetectorParameters_create()
MARKER_SIZE = 0.05  # Marker size in meters

# Camera class
class Camera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (1640, 1232)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()
        print("Camera initialized successfully")

    def capture(self):
        frame = self.cam.capture_array()
        return frame

    def release(self):
        self.cam.stop()

# Function to detect ArUco markers and calculate distance
def detect_and_calculate_distance(cam):
    frame = cam.capture()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Convert to grayscale for marker detection
    corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT, parameters=PARAMETERS)
    
    if ids is not None:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, MARKER_SIZE, camera_matrix, dist_coeffs)
        for i in range(len(ids)):
            distance = tvecs[i][0][2]
            print(f"Marker ID: {ids[i][0]} Distance: {distance:.2f} meters")
            aruco.drawDetectedMarkers(frame, corners)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)
        
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        return False
    return True

# Camera calibration parameters (example values)
camera_matrix = np.array([[628.679, 0, 314.221], [0, 628.679, 241.195], [0, 0, 1]])
dist_coeffs = np.array([0.0940, -0.2700, 0.0005, 0.0004, 0.0000])

# Initialize camera
try:
    cam = Camera()
except Exception as e:
    print(f"Failed to initialize camera: {e}")
    exit(1)

# Main loop
try:
    while True:
        if not detect_and_calculate_distance(cam):
            break
except KeyboardInterrupt:
    pass
finally:
    cam.release()
    cv2.destroyAllWindows()
