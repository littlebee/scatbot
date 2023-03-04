#!/usr/bin/env python3
import cv2


img = cv2.imread("tests/images/daphne-1.jpg")

# pretty sure this is a picture of daphne :), let's label it such
labeled_image = cv2.putText(
    img, "Daphne!", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 5, (128, 0, 255), 20
)

ret = cv2.imwrite("opencv-test-output.jpg", labeled_image)
if ret:
    print("Successfully saved")
else:
    print(f"Something went wrong.  ret from imwrite: {ret}")


print("you can view the image which should have a label, with:")
print(
    "   scp scatbot.local:/home/bee/scatbot/opencv-test-output.jpg . && open opencv-test-output.jpg"
)
print("on your local machine")
