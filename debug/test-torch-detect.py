#!/usr/bin/env python3

# stolen from https://github.com/spmallick/learnopencv/tree/master/PyTorch-faster-RCNN
# import necessary libraries
from PIL import Image
import cv2
import torchvision.transforms as T
import torchvision
import time


ANNOTATION_COLOR = (0, 128, 255)

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
    pretrained=True
)


model.eval()

# Class labels from official PyTorch documentation for the pretrained model
# Note that there are some N/A's
# for complete list check https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
# we will use the same list for this notebook
COCO_INSTANCE_CATEGORY_NAMES = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


def get_prediction(img_path, threshold):
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
    img = Image.open(img_path)
    transform = T.Compose([T.ToTensor()])
    t1 = time.time()
    img = transform(img)
    pred = model([img])
    t2 = time.time()
    print(f"took {t2 - t1}s for prediction {pred}")
    pred_class = [
        COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]["labels"].numpy())
    ]
    pred_boxes = [
        [(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]["boxes"].detach().numpy())
    ]
    pred_score = list(pred[0]["scores"].detach().numpy())
    pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
    pred_boxes = pred_boxes[: pred_t + 1]
    pred_class = pred_class[: pred_t + 1]
    return pred_boxes, pred_class


def main(img_path, threshold=0.5, rect_th=3, text_size=3, text_th=3):
    """
    object_detection_api
      parameters:
        - img_path - path of the input image
        - threshold - threshold value for prediction score
        - rect_th - thickness of bounding box
        - text_size - size of the class label text
        - text_th - thickness of the text
      method:
        - prediction is obtained from get_prediction method
        - for each prediction, bounding box is drawn and text is written
          with opencv
        - the final image is displayed
    """
    boxes, pred_cls = get_prediction(img_path, threshold)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for i in range(len(boxes)):
        topLeftPt = (int(boxes[i][0][0]), int(boxes[i][0][1]))
        bottomRightPt = (int(boxes[i][1][0]), int(boxes[i][1][1]))
        print(
            f"boxes {i} cls={pred_cls[i]} topLeftPt={topLeftPt} bottomRightPt={bottomRightPt}"
        )
        cv2.rectangle(
            img, topLeftPt, bottomRightPt, color=ANNOTATION_COLOR, thickness=rect_th
        )
        cv2.putText(
            img,
            pred_cls[i],
            topLeftPt,
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            ANNOTATION_COLOR,
            thickness=text_th,
        )

    # plt.figure(figsize=(20, 30))
    # plt.imshow(img)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()

    ret = cv2.imwrite("test-torch-detect-output.jpg", img)
    print("\n\n")
    if ret:
        print("Successfully saved")
    else:
        print(f"Something went wrong.  ret from imwrite: {ret}")

    print("you can view the image which have a labels on your local machine with:\n")
    print("scp scatbot.local:/home/bee/scatbot/test-torch-detect-output.jpg . && \\")
    print("open test-torch-detect-output.jpg")


if __name__ == "__main__":
    main("tests/images/daphne-1.jpg")

    # boxes, pred_cls = get_prediction("tests/images/daphne-1.jpg", threshold=0.5)
    # for i in range(len(boxes)):
    #     print(f"box0={boxes[i][0]} box1={boxes[i][1]} class={pred_cls[i]}")
