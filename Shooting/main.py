import logging

import cv2
import numpy as np
from parameters import param as parameters
from networktables import NetworkTables


def detect_hexagon(frame):
    return

def init_configures():
    try:
        # Initialize network table with roborio ip
        NetworkTables.initialize(server='10.56.35.2')
        # Initialize camera with given settings
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, parameters.CAM_WIDTH)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, parameters.CAM_HEIGHT)
        cam.set(cv2.CAP_PROP_FPS, 30)
        return cam
    except Exception as e:
        # Writes the exception into a logging file
        logging.error(e)
        # Calls itself until success
        init_configures()

def main():
    # Configs a logging file
    logging.basicConfig(filename='game.log', level=logging.DEBUG)
    # Camera and networktable configure
    cam = init_configures()
    # Gets the SmartDashboard table from networktables
    smartdashboard = NetworkTables.getTable("SmartDashboard")
    while cam.isOpened():
        _, frame = cam.read()

        # Fix fisheye
        frame = cv2.undistort(frame, parameters.CAMERA_MATRIX, parameters.DIST_COEFS, None)

        try:
            # Gets distance and angle from frame
            distance, angle = detect_hexagon(frame)
            # Insterts distance and angle in SmartDashboard
            smartdashboard.putNumber("Distance_Hexagon", distance)
            smartdashboard.putNumber("Angle_Hexagon", angle)
        except Exception as e:
            # Writes the exception into a logging file
            logging.error(e)

if __name__ == "__main__":
    main()
