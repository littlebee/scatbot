#
# I asked chatGPT, "generate python code make a robot that follows a pet".
# This is what it came up with.  Interesting ideas to follow up on.
#

import cv2

# Load the camera
cap = cv2.VideoCapture(0)

# Load the pet image
pet_img = cv2.imread('pet.jpg')

# Define the Haar Cascade for detecting the pet
pet_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')

# Set the robot's speed
robot_speed = 50

while True:
    # Read the camera frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the pet in the frame
    pets = pet_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If the pet is detected, follow it
    if len(pets) > 0:
        # Find the closest pet
        closest_pet = max(pets, key=lambda x: x[2])

        # Get the coordinates of the pet
        x, y, w, h = closest_pet

        # Calculate the center of the pet
        center_x = x + w // 2
        center_y = y + h // 2

        # Get the center of the frame
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

        # Calculate the difference between the pet center and the frame center
        delta_x = center_x - frame_center_x
        delta_y = center_y - frame_center_y

        # Control the robot based on the pet's position
        if delta_x < 0:
            # Pet is to the left of the frame, so turn left
            # code to turn the robot left
            pass
        elif delta_x > 0:
            # Pet is to the right of the frame, so turn right
            # code to turn the robot right
            pass
        else:
            # Pet is in the center of the frame, so move forward
            # code to move the robot forward
            pass

        # Adjust the robot's speed based on the pet's distance
        if w * h > 5000:
            # Pet is close, so slow down
            robot_speed = 30
        else:
            # Pet is far, so speed up
            robot_speed = 50

    # Show the frame
    cv2.imshow('frame', frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()

# Close the window
cv2.destroyAllWindows()