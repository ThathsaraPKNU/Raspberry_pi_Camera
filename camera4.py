import tkinter as tk
from tkinter import ttk
import cv2
import threading
from picamera2 import Picamera2

video0 = None
video1 = None
recording = False
cameras_open = False  # Flag to control the camera loop
cameras_thread = None  # Thread for the camera loop
resolution_720p = True  # Default resolution selection

def open_cameras():
    global cameras_open, cameras_thread
    try:
        if not cameras_open:
            # Create camera instances
            global cam1, cam2
            cam1 = camera(camera_index=0)
            cam2 = camera(camera_index=1)
            
            cameras_open = True
            cameras_thread = threading.Thread(target=camera_loop)
            cameras_thread.start()
    except Exception as e:
        print(f"Error opening cameras: {e}")

def camera_loop():
    global cameras_open
    while cameras_open:
        frame1 = cam1.capture()
        frame2 = cam2.capture()

        cv2.imshow('Cam 0', frame1)
        cv2.imshow('Cam 1', frame2)

        if cv2.waitKey(1) & 0xFF == ord('q') or not cameras_open:
            break
    cv2.destroyAllWindows()

def record_cameras():
    global recording
    recording = True
    record_thread = threading.Thread(target=record_loop)
    record_thread.start()
    recording_status_label.config(text="Recording...")

def record_loop():
    try:
        global recording, resolution_720p
        width, height = (1280, 720) if resolution_720p else (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out0 = cv2.VideoWriter('D:\\camera_0.avi', fourcc, 20.0, (width, height))
        out1 = cv2.VideoWriter('D:\\camera_1.avi', fourcc, 20.0, (width, height))
        while recording:
            frame0 = cam1.capture()
            frame1 = cam2.capture()
            
            out0.write(frame0)
            out1.write(frame1)
    except Exception as e:
        print(f"Error recording: {e}")

def stop_recording():
    global recording
    recording = False
    recording_status_label.config(text="Recording stopped.")

def release_cameras():
    global cameras_open, cameras_thread
    cameras_open = False
    if cameras_thread is not None:
        cameras_thread.join()
    cv2.destroyAllWindows()

def open_cameras_thread():
    open_cameras()

def close_cameras_and_stop_recording():
    stop_recording()
    release_cameras()

def resolution_selection_720p():
    global resolution_720p
    resolution_720p = True

def resolution_selection_1080p():
    global resolution_720p
    resolution_720p = False

class camera:
    def __init__(self, camera_index=0):
        self.cam = Picamera2(camera_num=camera_index)
        self.cam.preview_configuration.main.size = (1640, 1232)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

    def capture(self):
        frame = self.cam.capture_array()
        frame = cv2.resize(frame, (410, 308), interpolation=cv2.INTER_LINEAR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

TN = tk.Tk()
width, height = 300, 200
TN.geometry(f'{width}x{height}')
TN.title("Record Cameras")
TN.resizable(False, False)

open_button = ttk.Button(TN, text='Open Cameras', command=open_cameras_thread)
open_button.pack()

resolution_check_var_720p = tk.BooleanVar()
resolution_check_var_720p.set(True)  # Default selection
resolution_check_720p = ttk.Checkbutton(TN, text="720p", variable=resolution_check_var_720p, command=resolution_selection_720p)
resolution_check_720p.pack()

resolution_check_var_1080p = tk.BooleanVar()
resolution_check_var_1080p.set(False)  # Default selection
resolution_check_1080p = ttk.Checkbutton(TN, text="1080p", variable=resolution_check_var_1080p, command=resolution_selection_1080p)
resolution_check_1080p.pack()

record_button = ttk.Button(TN, text='Record', command=record_cameras)
record_button.pack()

recording_status_label = ttk.Label(TN, text="")
recording_status_label.pack()

stop_button = ttk.Button(TN, text='Stop Record', command=stop_recording)
stop_button.pack()

off_button = ttk.Button(TN, text='Off Cameras', command=close_cameras_and_stop_recording)
off_button.pack()

TN.mainloop()
