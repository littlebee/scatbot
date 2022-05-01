#!/usr/bin/env python3


# Python program to save a
# video using OpenCV
# from https://www.geeksforgeeks.org/saving-a-video-using-opencv/

import sys
import time
import cv2

video_channel = 0
if len(sys.argv) > 1:
    video_channel = int(sys.argv[1])


# Create an object to read
# from camera
video = cv2.VideoCapture(video_channel)

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)

print(f"starting VideoWriter video_channel={video_channel} size={size}", )

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
writer = cv2.VideoWriter('camera_test_output.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

start = time.time()
while(True):
    ret, frame = video.read()

    if ret == True:

        # Write the frame into the
        # file 'filename.avi'
        writer.write(frame)
        print('...wrote a frame to avi')

        # Display the frame
        # saved in the file
        # cv2.imshow('Frame', frame)

        cv2.waitKey(1)

    # Break the loop
    else:
        break

    # runs for 15
    if time.time() - start >= 15:
        break

# When everything done, release
# the video capture and video
# write objects
video.release()
writer.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")
