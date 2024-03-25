import cv2
import numpy as np

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to create a binary mask
    _, mask = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area (assuming it is the animal)
    largest_contour = max(contours, key=cv2.contourArea)

    # Create an empty mask and draw the largest contour on it
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest_contour], 0, (255), thickness=cv2.FILLED)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)

    return result

# Example usage
image_path = 'Resources/tuxedocat.jpg'
processed_image = preprocess_image(image_path)

# Display the processed image
cv2.imshow('Processed Image', processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
