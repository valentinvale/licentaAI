from rembg import remove
from PIL import Image
import cv2

def remove_background(image_path):
    input = cv2.imread(image_path)
    input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    output = remove(input)
    #output.show()
    return output
    