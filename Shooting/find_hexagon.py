import os
import cv2
import numpy as np
import parameters
import math


def find_distance(width):
    # calculate the distance
    return (parameters.BALL_WIDTH * parameters.FOCAL_LENGTH) / abs(width)


def detect_hexagon(frame):
    frame = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)  # By calibrated parameters

    # Blur the image to get a more reliable result of inRange
    blurred = cv2.GaussianBlur(frame, (3, 3), 0)

    # Convert to work in HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Masking and clearing the mask
    mask = cv2.inRange(hsv, parameters.MIN_HSV, parameters.MAX_HSV)
    cv2.imshow("mask1", mask)

    # mask = cv2.erode(mask, None, iterations=1)
    # mask = cv2.dilate(mask, None, iterations=1)

    cv2.imshow("mask2", mask)
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

            current_scale = width / parameters.BALL_WIDTH
            y_angle = (parameters.IMAGE_HEIGHT / 2 - loc[1]) / parameters.PIXEL_TO_DEGREES_RATIO
            x_angle = abs(parameters.IMAGE_WIDTH / 2 - loc[0]) / parameters.PIXEL_TO_DEGREES_RATIO
            dis = find_distance(width)
            width_mid = loc[0] - parameters.IMAGE_WIDTH / 2
            x_angle = math.atan((width_mid / current_scale) / dis) * 180 / math.pi

            return x_angle, y_angle, dis


def main():
    # Simple configuration for testing
    init()

    while cap.isOpened():
        ret, frame = cap.read()

        # fix the image
        frame = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)  # By calibrated parameters

        # Blur the image to get a more reliable result of inRange
        blurred = cv2.GaussianBlur(frame, (3, 3), 0)

        # Convert to work in HSV color space
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Masking and clearing the mask
        mask = cv2.inRange(hsv, parameters.MIN_HSV, parameters.MAX_HSV)
        cv2.imshow("mask1", mask)

        # mask = cv2.erode(mask, None, iterations=1)
        # mask = cv2.dilate(mask, None, iterations=1)

        cv2.imshow("mask2", mask)
        # Find contours of mask
        _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find center of mass only if found an object
        if len(contours) > 0:
            find_point(contours, frame)

        # draw the original frame
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(33) == ord('p'):
            print("picturing")
            file_count = os.listdir(r"C:/Users/Alut/PycharmProjects/FRC_2021_PreSeason/images")
            print("Number of Files using listdir method#1 :", len(file_count))
            cv2.imwrite("images/image_frc" + str(len(file_count)) + ".jpg", frame)
            print("took picture")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()