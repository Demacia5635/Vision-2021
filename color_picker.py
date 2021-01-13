import cv2
import numpy as np
import parameters
import subprocess
import json

# the minimum and maximum values (h, s, v)
min_hsv = [256, 256, 256]
max_hsv = [-1, -1, -1]

# אם זאת הלצחיצה הראשונה אז לא יצייר מלבן ויקח נתונים, אם לא, יצייר מלבן וייקח נתוני מינימום ומקסימום
first_click = True

# the x, y point for drawing the rectangle
lastX = -1
lastY = -1


def on_click(event, x, y, flags, param):
    """
    :param event: event type
    :param x: x pos
    :param y: y pos
    :param flags: not needed but must be param in the function
    :param param: not needed but must be param in the function
    :return: None
    """
    global lastY, lastX, first_click, min_hsv, max_hsv
    # check if the left button of the mouse clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # if this is the first press, save the x, y parameters to be able to use them to drw the rectangle
        if first_click:
            first_click = False
            lastY = y
            lastX = x

        # if this is the second press, get the max and min values inside the rectangle
        # draw rectangle with two circles on the pressed positions
        else:
            first_click = True

            # get the max and min values inside the rectangle
            roi = frame[min(y, lastY):max(y, lastY), min(x, lastX):max(x, lastX)].copy()
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            (h, s, v) = cv2.split(roi)
            min_hsv = [min(np.amin(h), min_hsv[0]), min(np.amin(s), min_hsv[1]), min(np.amin(v), min_hsv[2])]
            max_hsv = [max(np.amax(h), max_hsv[0]), max(np.amax(s), max_hsv[1]), max(np.amax(v), max_hsv[2])]

            # draw the rectangle with the two circles on the pressed positions
            output = cv2.rectangle(frame.copy(), (lastX, lastY), (x, y), (0, 255, 0), 2)
            output = cv2.circle(output, (lastX, lastY), 4, (0, 0, 255), -1)
            output = cv2.circle(output, (x, y), 4, (0, 0, 255), -1)

            # show the image
            cv2.imshow('frame', output)

            cv2.setTrackbarPos('H - max', 'tracker image', max_hsv[0])
            cv2.setTrackbarPos('S - max', 'tracker image', max_hsv[1])
            cv2.setTrackbarPos('V - max', 'tracker image', max_hsv[2])

            cv2.setTrackbarPos('H - min', 'tracker image', min_hsv[0])
            cv2.setTrackbarPos('S - min', 'tracker image', min_hsv[1])
            cv2.setTrackbarPos('V - min', 'tracker image', min_hsv[2])


def nothing(x):
    global h_max, s_max, v_max, h_min, s_min, v_min
    print("MAX_HSV = (" + str(h_max) + ",", str(s_max) + ",", str(v_max) + ")")
    print("MIN_HSV = (" + str(h_min) + ",", str(s_min) + ",", str(v_min) + ")", end="\n")


def main():
    global h_max, s_max, v_max, h_min, s_min, v_min, frame

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, parameters.IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, parameters.IMAGE_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while cap.isOpened():
        # get current positions of four trackbars
        h_max = cv2.getTrackbarPos('H - max', 'tracker image')
        s_max = cv2.getTrackbarPos('S - max', 'tracker image')
        v_max = cv2.getTrackbarPos('V - max', 'tracker image')

        h_min = cv2.getTrackbarPos('H - min', 'tracker image')
        s_min = cv2.getTrackbarPos('S - min', 'tracker image')
        v_min = cv2.getTrackbarPos('V - min', 'tracker image')

        ret, frame = cap.read()

        frame_with_detection = frame.copy()

        x, y, radius = detect_ball(frame)
        if x is not None and y is not None and radius is not None:
            frame_with_detection = cv2.circle(frame_with_detection, (int(x), int(y)), int(radius), (0, 0, 255), 2)
        cv2.imshow("frame_with_detection", frame_with_detection)

        # Convert to work in HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Masking and clearing the mask
        mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', img1_bg)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


def detect_ball(frame):
    x = None
    y = None
    radius = None
    image = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)
    blurred = cv2.GaussianBlur(image, (9, 9), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
    return x, y, radius


if __name__ == '__main__':
    # Create a black image, a window
    cv2.namedWindow('tracker image')
    cv2.resizeWindow('tracker image', 300, 250)

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_click)

    # create trackbars for color change
    cv2.createTrackbar('H - max', 'tracker image', 255, 255, nothing)
    cv2.createTrackbar('S - max', 'tracker image', 255, 255, nothing)
    cv2.createTrackbar('V - max', 'tracker image', 255, 255, nothing)

    cv2.createTrackbar('H - min', 'tracker image', 0, 255, nothing)
    cv2.createTrackbar('S - min', 'tracker image', 0, 255, nothing)
    cv2.createTrackbar('V - min', 'tracker image', 0, 255, nothing)

    h_max = 255
    s_max = 255
    v_max = 255
    h_min = 0
    s_min = 0
    v_min = 0
    main()
    inp = input("send parameters?")
    if inp.lower() == "y" or inp.lower() == "yes":
        process = subprocess.call(["scp", "pi@10.56.35.120:/home/pi/rcv/rcv/parameters.json", "./"])
        with open("parameters.json") as json_file:
            data = json.loads(json_file)
            data["MAX_HSV"] = (h_max, s_max, v_max)
            data["MIN_HSV"] = (h_min, s_min, v_min)
        with open('parameters.json', 'w') as json_file:
            json.dump(data, json_file)
        process = subprocess.call(["scp", "./parameters.json", "pi@10.56.35.120:/home/pi/rcv/rcv/"])