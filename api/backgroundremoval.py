from rembg import remove
from PIL import Image
import cv2
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

def remove_background(image_url):
    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    image_pil = Image.open(image_bytes)

    output = remove(np.array(image_pil))
    # decomentez pentru reglare
    # plt.imshow(output)
    # plt.show()
    return output
    