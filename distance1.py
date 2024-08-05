#Actual distance print, only 1 camera
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
    cam = Camera(camera_id=1)  # Camera 1
    
    while True:
        frame = cam.capture()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
        corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT, parameters=PARAMETERS)
        
        if ids is not None:
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, MARKER_SIZE, camera_matrix, dist_coeffs)
            aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Calculate and display the distance between bottom corners
            for i in range(len(ids)):
                # Get the bottom-left and bottom-right corners of the marker
                marker_corners = corners[i][0]
                bottom_left_corner = marker_corners[3]  # The bottom-left corner
                bottom_right_corner = marker_corners[2]  # The bottom-right corner
                
                # Convert to integer coordinates
                x1, y1 = int(bottom_left_corner[0]), int(bottom_left_corner[1])
                x2, y2 = int(bottom_right_corner[0]), int(bottom_right_corner[1])
                
                # Calculate the pixel distance between the bottom corners
                pixel_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                
                # Calculate the real distance using the given polynomial equation
                real_distance = calculate_real_distance(pixel_distance)
                
                # Draw and annotate the corners
                cv2.circle(frame, (x1, y1), 5, (0, 255, 0), -1)
                cv2.putText(frame, f"({x1}, {y1})", (x1 + 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                cv2.circle(frame, (x2, y2), 5, (0, 255, 0), -1)
                cv2.putText(frame, f"({x2}, {y2})", (x2 + 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                # Display the pixel distance on the frame
                midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
                cv2.putText(frame, f"Pixel Dist: {pixel_distance:.2f} px", (midpoint[0], midpoint[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                if real_distance is not None:
                    # Display the real distance on the frame
                    cv2.putText(frame, f"Real Dist: {real_distance:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                # Print the coordinates and distances
                print(f"Marker ID: {ids[i][0]} Bottom Left: ({x1}, {y1}), Bottom Right: ({x2}, {y2}), Pixel Distance: {pixel_distance:.2f} px, Real Distance: {real_distance:.2f} cm")
                
            # Display the frame with the distance annotation
            cv2.imshow("Distance Between Bottom Corners", frame)
        
        key = cv2.waitKey(1)
        if key == ord("c"):
            cv2.imwrite("/home/lab902/Documents/Camera Calibration/New Calibration/Aruco Markers/70cm/R1.jpg", frame)
        
        elif key == ord("q"):
            break

    cam.cam.stop()
    cv2.destroyAllWindows()
