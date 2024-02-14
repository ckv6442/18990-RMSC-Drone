# Written by Colin Vo
# Modified 2/14/24
# Reads from the serial port to determine which RFID reader.
# was the one that was tagged. Plays a video based on the reader.

import serial
import time
import cv2
from lib import moviepy
# import vlc

# Make sure to change the COM/USB port based on the OS and device
ser = serial.Serial(port='COM3', baudrate=115200)

# Infinite loop
while True:
    # If data is ready
    if ser.in_waiting > 0:
        # Read the data
        data = ser.readline()
        # Try to print the line
        try:
            print(data.decode("Ascii"))
            if (data.decode("Ascii").strip() == "0x24"):
                cap = cv2.VideoCapture("test.mp4")
                cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                # ret, frame = cap.read()
                while(1):
                   ret, frame = cap.read()

                   if not ret:
                       print("End of video, exiting.")
                       break
                   
                   cv2.imshow("window", frame)
                   
                   if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
                       break
                   # cv2.imshow('frame',frame)
                cap.release()
                cv2.destroyAllWindows()

        # If it errored out, it's probably just not good data, so pass
        except:
            pass
