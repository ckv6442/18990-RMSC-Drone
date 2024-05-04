#!/usr/bin/python
# -*- coding: utf-8 -*-

# Written by Colin Vo
# Modified 4/26/24
# Reads from the serial port to determine which RFID reader.
# was the one that was tagged. Plays a video based on the reader.

import serial
import time
import cv2
import PySimpleGUI as sg
import threading

# Logistic stuff
blocking = 0
ser = None
curr_vid = 0
num_videos = 3

# Determine what video is played next
def choose_video():
    global curr_vid
    if curr_vid == num_videos-1:
        curr_vid = 0
    else:
        curr_vid += 1
    return curr_vid

# Play the video normally. 
# If override is 1, then the "cheat" button was pressed
def play_video(override=0):
    global blocking
    # Read the data, block read if something is here
    try:
        data = ser.readline()
        print(data.decode('Ascii'))
        if data.decode('Ascii').strip() == '0x24':
           blocking = 1
    except:
        pass

    # Try to print the line
    if blocking or override:
       try:
           # Create the video
           cap = cv2.VideoCapture('vid' + str(choose_video()) + '.mp4')
           cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
           cv2.setWindowProperty('window',
           cv2.WND_PROP_FULLSCREEN,
           cv2.WINDOW_FULLSCREEN)

           # Read the video frame by frame
           # Play the video
           while (1):
               (ret, frame) = cap.read()

               if not ret:
                   print('End of video, exiting.')
                   break

               cv2.imshow('window', frame)

               # Quit if video is over or if 'q' is pressed
               if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
                   break

           # Release and destroy
           cap.release()
           cv2.destroyAllWindows()

           # Reset blocking
           blocking = 0
           
           # We've played the video, so we should flush so it doesn't replay
           ser.reset_input_buffer()

       # Exception handler
       except Exception as error:
       # If it errored out, it's probably just not good data, so pass
           print(error)
           pass

# "main" program over serial
def serial_main():
     # Make sure to change the COM/USB port based on the OS and device

     global ser
     ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

     # Infinite loop
     while True:
         # If data is ready
         if (ser.in_waiting > 0):
             play_video()


# GUI for image display. Kind of last minute solution, can definitely be cleaned up
# GUI has to be made in main thread because the library gives errors otherwise.
# Multithreading is used so the GUI/Serial aren't blocking each other
if __name__ == "__main__":
    # Create and start the thread to read in serial data
    serial_t = threading.Thread(target=serial_main)
    serial_t.start()

    # Create the layout, which consists of just an image. Can probably be fullscreened/expanded with other libraries
    # Also create the window which is just the layout but fullscreened.
    layout = [[sg.Image('bg.png', expand_x=True, expand_y=True)]]
    window = sg.Window('OVERRIDE', layout, return_keyboard_events=True, use_default_focus=True, size=(500, 500)).Finalize()
    window.Maximize()

    # Window event handler, common practice for PSG
    while True:
        event, values = window.read()
        print(event)

        # Override button was set to 'p'
        if event == 'p:33':
            print('PLAYING VIDEO')
            play_video(override=1)

        # Exit if Shift+q
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Shift_L:50':
            break

    # Close window and join threads
    window.close()
    serial_t.join()
