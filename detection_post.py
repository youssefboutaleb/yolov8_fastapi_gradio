####################################### IMPORT #################################
import json

import cv2
from loguru import logger
import sys
from starlette.responses import Response, HTMLResponse

from fastapi import FastAPI, APIRouter, File ,Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

import io
from PIL import Image
from starlette.templating import Jinja2Templates

from yolov8 import get_image_from_bytes
from yolov8 import detect_sample_model
from yolov8 import add_bboxs_on_img
from yolov8 import get_bytes_from_image

router = APIRouter(prefix='/detection', tags=['Detection'])


######################### MAIN Func #################################


@router.post("/img_object_detection_to_json")
def img_object_detection_to_json(file: bytes = File(...)):
    """
    **Object Detection from an image.**

    **Args:**
        - **file (bytes)**: The image file in bytes format.
    **Returns:**
        - **dict**: JSON format containing the Objects Detections.
    """
    # Step 1: Initialize the result dictionary with None values
    result={'detect_objects': None}

    # Step 2: Convert the image file to an image object
    input_image = get_image_from_bytes(file)

    # Step 3: Predict from model
    predict = detect_sample_model(input_image)

    # Step 4: Select detect obj return info
    # here you can choose what data to send to the result
    detect_res = predict[['name', 'confidence']]
    objects = detect_res['name'].values

    result['detect_objects_names'] = ', '.join(objects)
    result['detect_objects'] = json.loads(detect_res.to_json(orient='records'))

    # Step 5: Logs and return
    logger.info("results: {}", result)
    return result
templates = Jinja2Templates(directory="templates")
@router.get("/description", response_class=HTMLResponse)
def read_description(request: Request):
    return templates.TemplateResponse("description.html", {"request": request})

@router.post("/img_object_detection_to_img")
def img_object_detection_to_img(request: Request, file: bytes = File(...)):
    """
    Object Detection from an image plot bbox on image

    Args:
        - file (bytes): The image file in bytes format.
    Returns:
        - Image: Image in bytes with bbox annotations.
    """
    # get image from bytes
    input_image = get_image_from_bytes(file)

    # model predict
    predict = detect_sample_model(input_image)

    # add bbox on image
    final_image = add_bboxs_on_img(image=input_image, predict=predict)

    # save image to a file
    image_path = "static/src/imgresult.jpg"
    final_image.save(image_path)



    # Select detect obj return info
    # Include 'xmin' in the prediction results to get the x-coordinate of the bounding box
    detect_res = predict[['name', 'confidence', 'xmin']]

    # Sort the results by 'xmin' to order them from left to right
    sorted_detect_res = detect_res.sort_values(by='xmin')



    # Extract only the names (numbers) from the sorted results
    sorted_numbers = sorted_detect_res['name'].tolist()

    # Update the result dictionary


    # Logs and return
    logger.info("results: {}", sorted_numbers)

    # return HTML page with the image and sorted results
    return templates.TemplateResponse("result.html",
                                      {"request": request, "image_path": "../" + image_path, "result": ''.join(sorted_numbers)})

# Additional helper functions like get_image_from_bytes, detect_sample_model, and add_bboxs_on_img should be defined elsewhere in your code.
