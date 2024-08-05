#Overlap the camera,distance 45cm

from picamera2 import Picamera2, Preview
from time import sleep
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
        # No resizing
        
        return frame

if __name__ == "__main__":
    # Initialize cameras
    cam0 = Camera(camera_id=0)
    cam1 = Camera(camera_id=1)
    
    while True:
        # Capture frames from both cameras
        frame0 = cam0.capture()
        frame1 = cam1.capture()
        
        # Define the translation matrix for camera 0
        tx, ty = -151, 46  #tx, ty = -151, 46
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        
        # Translate the frame from camera 0
        frame0_translated = cv2.warpAffine(frame0, translation_matrix, (frame0.shape[1], frame0.shape[0]))
        
        # Create a mask for the translated frame from camera 0
        mask = cv2.threshold(cv2.cvtColor(frame0_translated, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY)[1]
        
        # Apply the mask to camera 1's frame
        frame1_with_mask = cv2.bitwise_and(frame1, frame1, mask=mask.astype(np.uint8))
        
        # Merge the frames
        merged_frame = cv2.addWeighted(frame0_translated, 0.5, frame1_with_mask, 0.5, 0)
        
        # Display the merged frame
        cv2.imshow("Merged Frames", merged_frame)
        
        if cv2.waitKey(1) == ord("q"):
            break

    # Release resources
    cv2.destroyAllWindows()