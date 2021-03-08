import cv2
import math
from math import tan, atan2
import numpy as np
import parameters


data = {
    "x_angle": 0,
    "y_angle": 0,
    "distance": 0
}


def detect_hexa(frame, width_given):
    frame = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)  # By calibrated parameters
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Blur the image to get a more reliable result of inRange
    blurred = cv2.GaussianBlur(frame, (3, 3), 0)

    # Convert to work in HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Masking and clearing the mask
    mask = cv2.inRange(hsv, parameters.MIN_HSV, parameters.MAX_HSV)
    # Find contours of mask
    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find center of mass only if found an object
    if len(contours) > 0:
        approx = []
        for contour in contours:
            if 0 < cv2.contourArea(contour) < 10000000:
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx_current = cv2.approxPolyDP(contour, epsilon, True)
                if 6 < len(approx_current) < 12:
                    approx.append(approx_current)

        if len(approx) > 0:
            chosen = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(chosen)
            box = cv2.boxPoints(rect)
            box = np.array(box).reshape((-1, 1, 2)).astype(np.int32)

            m = (box[2][0][1] - box[0][0][1]) / (box[2][0][0] - box[0][0][0])

            if m < 0:
                loc = (int((box[1][0][0] + box[2][0][0]) / 2), int((box[1][0][1] + box[2][0][1]) / 2))
                width = box[2][0][0] - box[1][0][0]
            else:
                loc = (int((box[2][0][0] + box[3][0][0]) / 2), int((box[2][0][1] + box[3][0][1]) / 2))
                width = box[2][0][0] - box[3][0][0]

            current_scale = width / parameters.HEXAGON_WIDTH
            y_angle = abs(parameters.IMAGE_HEIGHT / 2 - loc[1]) / parameters.PIXEL_TO_DEGREES_RATIO_Y
            x_angle = abs(width / 2 - loc[0]) / parameters.PIXEL_TO_DEGREES_RATIO_X
            dis = find_distance(width)
            width_mid = loc[0] - width / 2
            x_angle = math.atan((width_mid / current_scale) / dis) * 180 / math.pi

            data["x_angle"] = x_angle
            data["y_angle"] = y_angle
            data["distance"] = dis

            return data, (x_angle, y_angle, dis)
    return None, (0, 0, 0)

def find_distance(width):
    return (parameters.HEXAGON_WIDTH * parameters.FOCAL_LENGTH) / abs(width)


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