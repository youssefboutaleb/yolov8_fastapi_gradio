import cv2
import numpy as np
from sahi.utils.cv import read_image_as_pil,get_bool_mask_from_coco_segmentation
from sahi.prediction import ObjectPrediction, PredictionScore,visualize_object_predictions
from PIL import Image
def custom_render_result(model,image, result,rect_th=2,text_th=2):
    if model.overrides["task"] not in ["detect", "segment"]:
        raise ValueError(
            f"Model task must be either 'detect' or 'segment'. Got {model.overrides['task']}"
        )

    image = read_image_as_pil(image)
    np_image = np.ascontiguousarray(image)

    names = model.model.names

    masks = result.masks
    boxes = result.boxes

    object_predictions = []
    if boxes is not None:
        det_ind = 0
        for xyxy, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            if masks:
                img_height = np_image.shape[0]
                img_width = np_image.shape[1]
                segments = masks.segments
                segments = segments[det_ind]  # segments: np.array([[x1, y1], [x2, y2]])
                # convert segments into full shape
                segments[:, 0] = segments[:, 0] * img_width
                segments[:, 1] = segments[:, 1] * img_height
                segmentation = [segments.ravel().tolist()]

                bool_mask = get_bool_mask_from_coco_segmentation(
                    segmentation, width=img_width, height=img_height
                )
                if sum(sum(bool_mask == 1)) <= 2:
                    continue
                object_prediction = ObjectPrediction.from_coco_segmentation(
                    segmentation=segmentation,
                    category_name=names[int(cls)],
                    category_id=int(cls),
                    full_shape=[img_height, img_width],
                )
                object_prediction.score = PredictionScore(value=conf)
            else:
                object_prediction = ObjectPrediction(
                    bbox=xyxy.tolist(),
                    category_name=names[int(cls)],
                    category_id=int(cls),
                    score=conf,
                )
            object_predictions.append(object_prediction)
            det_ind += 1

    result = visualize_object_predictions(
        image=np_image,
        object_prediction_list=object_predictions,
        rect_th=rect_th,
        text_th=text_th,
    )

    return Image.fromarray(result["image"])