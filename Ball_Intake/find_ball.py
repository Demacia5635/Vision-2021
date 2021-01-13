import cv2
from math import tan, atan2
import numpy as np
import parameters


data = {
    "angle": 0,
    "distance": 0
}


def find_angle(px):
    horizontal_fov = 26
    nx = (1 / 160) * (px - 159.5)
    vpw = 2.0 * tan(horizontal_fov / 2)
    x = vpw / 2 * nx
    ax = atan2(x, 1)
    return float(np.degrees(ax))


def detect_ball(frame):
    image = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)
    blurred = cv2.GaussianBlur(image, (9, 9), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, parameters.MIN_HSV, parameters.MAX_HSV)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        data["angle"] = round(find_angle(x))
        data["distance"] = round(find_dis(radius))
        return data


def find_dis(radius):
    return (18 * 320) / (radius * 2)


def init():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 30)


if __name__ == '__main__':
    init()
    while cap.isOpened():
        _, img = cap.read()
        #  find_ball_simple()
        cv2.imshow("Frame", img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()