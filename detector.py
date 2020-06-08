import cv2
import numpy as np
import urllib.request


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


# Load image, grayscale, Otsu's threshold
image = url_to_image(
    'https://res.cloudinary.com/cascadia/image/upload/v1590943353/QuizMe/Images/index_o5zjrt.png')
# image = cv2.imread('test.png')
# image = cv2.imread('test2.png')
# image = cv2.imread('index1.jpg')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# # Dilate with horizontal kernel
# # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,10))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 2))
dilate = cv2.dilate(thresh, kernel, iterations=2)

# Find contours and remove non-diagram contours
# contours, hierarchy = cv2.findContours(thresh,
#     cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Iterate through diagram contours and form single bounding box
# boxes = []
# cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# for c in cnts:
#     x, y, w, h = cv2.boundingRect(c)
#     area = cv2.contourArea(c)
#     if w/h > 2 and area > 10000:
#         print("found")
#         boxes.append([x, y, x+w, y+h])
#         cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)

boxes = []
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    if w/h > 2 and area > 10000:
        print("found")
        boxes.append([x, y, x+w, y+h])
        cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)


if(boxes):
    boxes = np.asarray(boxes)
    print('Diagram found', boxes.shape)
    x = np.min(boxes[:, 0])
    y = np.min(boxes[:, 1])
    w = np.max(boxes[:, 2]) - x
    h = np.max(boxes[:, 3]) - y
    print(x, y, w, h)
    # # Extract ROI
cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
ROI = original[y:y+h, x:x+w]

# # cv2.imshow('image', gray)
# cv2.imshow('thresh', thresh)
# cv2.imshow('dilate', dilate)
# cv2.imshow('ROI', ROI)
# cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)
# cv2.imshow('Contours', image)
# cv2.waitKey(0)
# cv2.waitKey()
