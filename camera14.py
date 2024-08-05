#normal open camera0

import cv2
from picamera2 import Picamera2

DEFAULT_RESOLUTION = (1640, 1232)

def main():
    try:
        # Initialize Camera 0 (cam0) with default resolution
        cam1 = Camera(camera_index=0, resolution=DEFAULT_RESOLUTION)
        
        # Main loop to capture and display frames from cam0
        while True:
            frame = cam1.capture()
            cv2.imshow('Cam 0', frame)
            
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Clean up
        cam1.release()
        cv2.destroyAllWindows()
    
    except Exception as e:
        print(f"Error: {e}")

class Camera:
    def __init__(self, camera_index=0, resolution=DEFAULT_RESOLUTION):
        self.cam = Picamera2(camera_num=camera_index)
        self.cam.preview_configuration.main.size = resolution
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

    def capture(self):
        frame = self.cam.capture_array()
        return frame

    def release(self):
        self.cam.stop()

if __name__ == "__main__":
    main()
