#corner detection cordinates show real time

from picamera2 import Picamera2
import cv2
import numpy as np

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

if __name__ == "__main__":
    # Initialize camera
    cam = Camera(camera_id=1)  # Camera 1
    
    while True:
        # Capture frame from camera 1
        frame = cam.capture()
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Detect corners using Shi-Tomasi corner detection
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
        
        if corners is not None:
            corners = np.int0(corners)
            
            # Draw detected corners on the frame and display their coordinates
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"({x}, {y})", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
            # Display the frame with detected corners
            cv2.imshow("Corners Detected", frame)
        
        # Check for 'c' key press to capture the frame with corners
        key = cv2.waitKey(1)
        if key == ord("c"):
            # Save the captured frame with detected corners
            cv2.imwrite("/home/lab902/Documents/Stereo 2/Photos/R10.jpg", frame)
            
            # Print the coordinates of detected corners
            if corners is not None:
                print("Detected corners coordinates (x, y):")
                for corner in corners:
                    x, y = corner.ravel()
                    print(f"({x}, {y})")
            else:
                print("No corners detected.")
        
        # Check for 'q' key press to quit the loop
        elif key == ord("q"):
            break

    # Release resources
    cam.cam.stop()
    cv2.destroyAllWindows()
