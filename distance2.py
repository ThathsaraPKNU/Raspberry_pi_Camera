##Actual distance print, both cameras
import cv2
import cv2.aruco as aruco
import numpy as np
from picamera2 import Picamera2
import math

# Define ArUco dictionary and parameters
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
PARAMETERS = aruco.DetectorParameters_create()
MARKER_SIZE = 0.05  # Marker size in meters

# Camera calibration parameters (example values)
camera_matrix = np.array([[628.679, 0, 314.221], [0, 628.679, 241.195], [0, 0, 1]])
dist_coeffs = np.array([0.0940, -0.2700, 0.0005, 0.0004, 0.0000])

class Camera:
    def __init__(self, camera_id):
        self.cam = Picamera2(camera_id)
        self.cam.preview_configuration.main.size = (1640, 1232)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

    def capture(self):
        frame = self.cam.capture_array()
        return frame

    def stop(self):
        self.cam.stop()

def calculate_real_distance(pixel_distance):
    # Coefficients of the polynomial equation
    coefficients = [-8.38e-03, 1.13e+00, -5.30e+01, 1.00e+03 - pixel_distance]
    
    # Find the roots of the polynomial equation
    roots = np.roots(coefficients)
    
    # The real distance is the positive root
    real_distance = np.real(roots[np.isreal(roots) & (roots > 0)])
    
    if len(real_distance) > 0:
        return real_distance[0]
    else:
        return None

if __name__ == "__main__":
    try:
        cam0 = Camera(camera_id=0)  # Initialize cam 0
        cam1 = Camera(camera_id=1)  # Initialize cam 1
    except Exception as e:
        print(f"Error initializing cameras: {e}")
        exit()

    cv2.namedWindow('Camera 0', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Camera 1', cv2.WINDOW_NORMAL)

    while True:
        try:
            frame0 = cam0.capture()
            frame1 = cam1.capture()

            if frame0 is None or frame1 is None:
                print("Error capturing frames from one or more cameras.")
                break

            # Process frames from cam 0
            gray0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
            corners0, ids0, _ = aruco.detectMarkers(gray0, ARUCO_DICT, parameters=PARAMETERS)

            if ids0 is not None:
                for i in range(len(ids0)):
                    # Calculate pixel distance for cam 0
                    marker_corners = corners0[i][0]
                    bottom_left_corner = marker_corners[3]
                    bottom_right_corner = marker_corners[2]
                    x1, y1 = int(bottom_left_corner[0]), int(bottom_left_corner[1])
                    x2, y2 = int(bottom_right_corner[0]), int(bottom_right_corner[1])
                    pixel_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    real_distance = calculate_real_distance(pixel_distance)

                    # Draw distance information on frame 0
                    cv2.circle(frame0, (x1, y1), 5, (0, 255, 0), -1)
                    cv2.putText(frame0, f"({x1}, {y1})", (x1 + 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    cv2.circle(frame0, (x2, y2), 5, (0, 255, 0), -1)
                    cv2.putText(frame0, f"({x2}, {y2})", (x2 + 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
                    cv2.putText(frame0, f"Pixel Dist: {pixel_distance:.2f} px", (midpoint[0], midpoint[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    if real_distance is not None:
                        cv2.putText(frame0, f"Real Dist: {real_distance:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Print distance for cam 0
                    print(f"Camera 0 - Marker ID: {ids0[i][0]} Pixel Distance: {pixel_distance:.2f} px, Real Distance: {real_distance:.2f} cm")

            # Process frames from cam 1
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
            corners1, ids1, _ = aruco.detectMarkers(gray1, ARUCO_DICT, parameters=PARAMETERS)

            if ids1 is not None:
                for i in range(len(ids1)):
                    # Calculate pixel distance for cam 1
                    marker_corners = corners1[i][0]
                    bottom_left_corner = marker_corners[3]
                    bottom_right_corner = marker_corners[2]
                    x1, y1 = int(bottom_left_corner[0]), int(bottom_left_corner[1])
                    x2, y2 = int(bottom_right_corner[0]), int(bottom_right_corner[1])
                    pixel_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    real_distance = calculate_real_distance(pixel_distance)

                    # Draw distance information on frame 1
                    cv2.circle(frame1, (x1, y1), 5, (0, 255, 0), -1)
                    cv2.putText(frame1, f"({x1}, {y1})", (x1 + 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    cv2.circle(frame1, (x2, y2), 5, (0, 255, 0), -1)
                    cv2.putText(frame1, f"({x2}, {y2})", (x2 + 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
                    cv2.putText(frame1, f"Pixel Dist: {pixel_distance:.2f} px", (midpoint[0], midpoint[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    if real_distance is not None:
                        cv2.putText(frame1, f"Real Dist: {real_distance:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Print distance for cam 1
                    print(f"Camera 1 - Marker ID: {ids1[i][0]} Pixel Distance: {pixel_distance:.2f} px, Real Distance: {real_distance:.2f} cm")

            # Display frames from both cameras
            cv2.imshow('Camera 0', frame0)
            cv2.imshow('Camera 1', frame1)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        except Exception as e:
            print(f"Error processing frames: {e}")
            break

    cam0.stop()
    cam1.stop()
    cv2.destroyAllWindows()
