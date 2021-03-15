# ----------------------------------------------------- Imports ----------------------------------------------------- #
import cv2
import numpy as np
import parameters
import xlwt
from xlwt import Workbook
# ------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------- Data Insertion Function --------------------------------------------- #
def insert_data(distance_data):
    if len(distance_data) > 0:
        distance_data = sorted(distance_data, key=lambda x: x[0])
        for i in range(len(distance_data)):
            sheet.write(i + 1, 0, distance_data[i][1], style)
            sheet.write(i + 1, 1, distance_data[i][0], style)
    workbook.save(f"{cam}_{mode}_calc.xls")
# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------ Detection Function ----------------------------------------------- #
def find_data(frame):
    frame = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)  # By calibrated parameters

    # Blur the image to get a more reliable result of inRange
    blurred = cv2.GaussianBlur(frame, (3, 3), 0)

    # Convert to work in HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Masking and clearing the mask
    mask = cv2.inRange(hsv, parameters.MIN_HSV, parameters.MAX_HSV)
    cv2.imshow("mask1", mask)

    # Find contours of mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find center of mass only if found an object
    if len(contours) > 0:
        approx = []
        for contour in contours:
            if cv2.contourArea(contour) > 0:
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx_current = cv2.approxPolyDP(contour, epsilon, True)
                if 6 < len(approx_current) < 12:
                    approx.append(approx_current)

        if len(approx) > 0:
            # Find the biggest countour (c) by the area
            c = max(approx, key=cv2.contourArea)
            cv2.drawContours(frame, [c], 0, (0, 0, 255), 2)
            cv2.imshow('_detected', frame)
            if cam == 'h':
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.array(box).reshape((-1, 1, 2)).astype(np.int32)

                # Draw rectangle points
                i = 1
                for point in box:
                    cv2.putText(frame, str(i), (point[0][0], point[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                                cv2.LINE_AA)
                    i += 1

                # Box center calculation
                m = (box[2][0][1] - box[0][0][1]) / (box[2][0][0] - box[0][0][0])

                if m < 0:
                    width = box[2][0][0] - box[1][0][0]
                    center = (box[2][0][0] + box[1][0][0]) / 2
                else:
                    width = box[2][0][0] - box[3][0][0]
                    center = (box[2][0][0] + box[3][0][0]) / 2

                return abs(float(width))if mode == 'd' else center
            else:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                return abs(float(radius)) if mode == 'd' else x

    return None
# ------------------------------------------------------------------------------------------------------------------- #


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Global variables assignment
    global sheet, style, cam, mode

    # Excel setup
    workbook = Workbook()
    sheet = workbook.add_sheet("Camera proportion")
    style = xlwt.easyxf('font: bold 1')

    # Either hexagon or ball cameras are available
    cam = input("What camera is it for? (h/b)")
    while not (cam == 'h' or cam == 'b'):
        cam = input("What camera is it for? (h/b)")
    # Either distance or angle cameras are available
    mode = input("What function are you trying to create? (d/a)")
    while not(mode == 'd' or mode == 'a'):
        mode = input("What function are you trying to create? (d/a)")
    sheet.write(0, 0, '{}'.format("Width" if mode == 'd' else "Delta(x)"), style)
    sheet.write(0, 1, '{}'.format("Distance" if mode == 'd' else "Angle"), style)

    # Video and variable setup
    excel_data = []
    cap = cv2.VideoCapture(0)

    print("Press Space to stop camera and measure distance")
    print("Press d to delete un-wanted input")
    print("Press Esc to exit and save the data to excel file")

    # While loop for capturing video
    while cap.isOpened():
        _, img = cap.read()

        # Get width of enclosing rectangle from frame
        data = find_data(img)

        cv2.imshow('org_frame', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            insert_data(excel_data)
            break
        elif k == 32:
            if data is not None:
                excel_data.append((float(input("Please input current {}: ".format("distance" if mode == 'd'
                                                                                  else "angle"))), data))
        elif k == ord('d'):
            if len(excel_data) > 0:
                excel_data.pop()

    cv2.destroyAllWindows()
