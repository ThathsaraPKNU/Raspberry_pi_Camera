from picamera2 import Picamera2, Preview
from time import sleep
import cv2


class camera:
    def __init__(self, camera_index=0):
        self.cam = Picamera2(camera_num=camera_index)
        self.cam.preview_configuration.main.size=(1640, 1232)
        self.cam.preview_configuration.main.format="RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

    def capture(self):
        frame=self.cam.capture_array()
        frame = cv2.resize(frame, (410,308),interpolation=cv2.INTER_LINEAR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame



if __name__ == "__main__":
    # Create two camera instances, one for each camera index
    cam1 = camera(camera_index=0)
    cam2 = camera(camera_index=1)

    while True:
        # Capture frames from both cameras
        frame1 = cam1.capture()
        frame2 = cam2.capture()

        # Display frames from both cameras
        cv2.imshow("Camera 1", frame1)
        cv2.imshow("Camera 2", frame2)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
