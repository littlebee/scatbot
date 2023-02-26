"""
This class provides object detection using Tensor Flow Lite.
"""
import logging

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


from commons import constants as c

logger = logging.getLogger(__name__)


class TFLiteDetect:
    detector = None

    def __init__(self):
        # Initialize the object detection model
        model = None
        if c.DISABLE_CORAL_TPU:
            # # this is the model from tensor flow hub
            # model = f"{TFLITE_DATA_DIR}/efficientdet_lite0.tflite"

            # this is the model from coral web site
            model = (
                f"{c.TFLITE_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess.tflite"
            )
        else:
            # model = f"{TFLITE_DATA_DIR}/efficientdet_lite0_edgetpu.tflite"
            model = f"{c.TFLITE_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite"

        print(f"using model {model}")

        base_options = core.BaseOptions(
            file_name=model,
            use_coral=(not c.DISABLE_CORAL_TPU),
            num_threads=c.TFLITE_THREADS,
        )
        detection_options = processor.DetectionOptions(
            max_results=3, score_threshold=0.3
        )
        options = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options
        )
        self.detector = vision.ObjectDetector.create_from_options(options)

    def get_prediction(self, img):
        input_tensor = vision.TensorImage.create_from_array(img)
        detection_result = self.detector.detect(input_tensor)
        results = []
        if detection_result.detections:
            for detection in detection_result.detections:
                bestClassification = max(detection.classes, key=lambda x: x.score)
                results.append(
                    {
                        "boundingBox": [
                            detection.bounding_box.origin_x,
                            detection.bounding_box.origin_y,
                            detection.bounding_box.origin_x
                            + detection.bounding_box.width,
                            detection.bounding_box.origin_y
                            + detection.bounding_box.height,
                        ],
                        "classification": bestClassification.class_name,
                        "confidence": bestClassification.score,
                    }
                )

        return results
