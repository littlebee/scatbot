"""
This class provides object detection using Tensor Flow Lite.
"""
import asyncio
import logging
import os

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


from commons import constants

logger = logging.getLogger(__name__)


# use coral USB tpu
ENABLE_CORAL_TPU = True if not os.getenv(
    'ENABLE_CORAL_TPU') else bool(int(os.getenv('ENABLE_CORAL_TPU')))

# num cpu threads to use for tensor flow lite
TFLITE_THREADS = 4 if not os.getenv(
    'TFLITE_THREADS') else int(os.getenv('TFLITE_THREADS'))

TFLITE_DATA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../data/tflite'))


class TFLiteDetect:
    detector = None

    def __init__(self):
        # Initialize the object detection model
        model = None
        if ENABLE_CORAL_TPU:
            model = f"{TFLITE_DATA_DIR}/efficientdet_lite0_edgetpu.tflite"
        else:
            model = f"{TFLITE_DATA_DIR}/efficientdet_lite0.tflite"

        print(f"using model {model}")

        base_options = core.BaseOptions(
            file_name=model, use_coral=ENABLE_CORAL_TPU, num_threads=TFLITE_THREADS)
        detection_options = processor.DetectionOptions(
            max_results=3, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options)
        self.detector = vision.ObjectDetector.create_from_options(options)

    def get_prediction(self, img):
        input_tensor = vision.TensorImage.create_from_array(img)
        detection_result = self.detector.detect(input_tensor)
        results = []
        if detection_result.detections:
            for detection in detection_result.detections:
                bestClassification = max(
                    detection.classes, key=lambda x: x.score)
                results.append({
                    "boundingBox": [
                        detection.bounding_box.origin_x,
                        detection.bounding_box.origin_y,
                        detection.bounding_box.origin_x + detection.bounding_box.width,
                        detection.bounding_box.origin_y + detection.bounding_box.height,
                    ],
                    "classification": bestClassification.class_name,
                    "confidence": bestClassification.score
                })

        return results
