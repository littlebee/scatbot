#!/usr/bin/env python3

# stolen from https://github.com/spmallick/learnopencv/tree/master/PyTorch-faster-RCNN
# import necessary libraries
import cv2
import torchvision.transforms as T
import torchvision
import sys
import time


from commons import constants


# get the pretrained model from torchvision.models
# Note: pretrained=True will get the pretrained weights for the model.
# model.eval() to use the model for inference

# # By far the slowest on test image.  By far the most sensitive, it can
# # can see the car out of the window, but also predicts that Daphne's mouth
# # is a "remote":)  21s on the old macbook (cpu); 35 seconds on the PI 4b:
# model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

# # Faster, but less accurate. Returns daphne as both cat and dog.
# model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(
#     pretrained=True)

# # Faster and accurate. Also less sensitive - only detects one object "dog"
# # 0.59s on macbook cpu; 2.11s on PI 4b:
model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(
    pretrained=True)


model.eval()

transform = T.Compose([T.ToTensor()])


def get_prediction(img, threshold):
    """
    get_prediction
      parameters:
        - img_path - path of the input image
        - threshold - threshold value for prediction score
      method:
        - Image is obtained from the image path
        - the image is converted to image tensor using PyTorch's Transforms
        - image is passed through the model to get the predictions
        - class, box coordinates are obtained, but only prediction score > threshold
          are chosen.

    """

    img = transform(img)
    pred = model([img])
    pred_class = [constants.COCO_INSTANCE_CATEGORY_NAMES[i]
                  for i in list(pred[0]['labels'].numpy())]
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])]
                  for i in list(pred[0]['boxes'].detach().numpy())]
    pred_score = list(pred[0]['scores'].detach().numpy())
    pred_t = [pred_score.index(x) for x in pred_score if x > threshold]
    if len(pred_t):
        pred_boxes = pred_boxes[:pred_t[-1]+1]
        pred_class = pred_class[:pred_t[-1]+1]
        return pred_boxes, pred_class
    else:
        return [], []


def main(source=constants.CAMERA_CHANNEL_RGB, threshold=0.5, rect_th=3, text_size=3, text_th=3):
    """
      parameters:
        - threshold - threshold value for prediction score
        - rect_th - thickness of bounding box
        - text_size - size of the class label text
        - text_th - thichness of the text
    """

    print(f"starting video capture. source={source}")

    video = cv2.VideoCapture(source)

    # We need to check if camera is opened previously or not
    if (video.isOpened() == False):
        print("Error creating video capture")

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)

    frames = 0
    while True:
        # read frame
        ret, image = video.read()
        if not ret:
            raise RuntimeError(f"failed to read frame. ret={ret}")

        t1 = time.time()
        boxes, pred_cls = get_prediction(image, threshold)
        t2 = time.time()
        frames += 1

        print(f"{frames}: boxes={boxes} pred_cls={pred_cls} ({t2 - t1}s)")


if __name__ == "__main__":
    source = int(sys.argv[1]) if len(
        sys.argv) > 1 else constants.CAMERA_CHANNEL_RGB
    main(source)
