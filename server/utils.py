import base64
import os

def save_image(image_data, image_path):
    with open(image_path, "wb") as fh:
        fh.write(base64.b64decode(image_data))
