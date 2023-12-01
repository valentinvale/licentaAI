import cv2
import numpy as np

img = cv2.imread('Resources/tuxedocat.jpg')
cv2.imshow('Original', img)
cv2.waitKey(0)

print(img.shape)

twoDim = img.reshape((-1, 3))

print(twoDim.shape)

twoDim = np.float32(twoDim)

print(twoDim)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

K = 2
attempts = 10

ret, label, center = cv2.kmeans(twoDim, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)

center = np.uint8(center)

res = center[label.flatten()]

resultImage = res.reshape((img.shape))

cv2.imshow('Result', resultImage)
cv2.waitKey(0)
cv2.destroyAllWindows()