import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(20, 200)

mycolors = [[0, 77, 122, 179, 255, 255]]  # Corrected array syntax
myvalues = [[127, 0, 255]]  # BGR format
mypoints = []  # [x,y,colorid]

def findcolor(img, mycolors, myvalues):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in mycolors:
        lower = np.array(color[0:3], dtype=np.uint8)  # Ensure proper data type
        upper = np.array(color[3:6], dtype=np.uint8)  # Ensure proper data type
        mask = cv2.inRange(imghsv, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            newpoints.append([x, y, count])
        count += 1
    return newpoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y + h // 2  # Return center coordinates

def drawoncanvas(mypoints, myvalues, imgResult):
    for points in mypoints:
        cv2.circle(imgResult, (points[0], points[1]), 10, myvalues[points[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = findcolor(img, mycolors, myvalues)
    if len(newpoints) != 0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(newpoints) != 0:
        drawoncanvas(mypoints, myvalues, imgResult)
    cv2.imshow('Result', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
