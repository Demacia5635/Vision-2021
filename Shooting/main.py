import logging

import cv2
import numpy as np
import parameters
from networktables import NetworkTables


def detect_hexagon(frame):
    return

def init_configures():
    try:
        NetworkTables.initialize(server='10.56.35.2')
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, parameters.CAM_WIDTH)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, parameters.CAM_HEIGHT)
        cam.set(cv2.CAP_PROP_FPS, 30)
        return cam
    except Exception as e:
        logging.error(e)
        init_camera()

def main():
    logging.basicConfig(filename='game.log', encoding='utf-8', level=logging.DEBUG)
    cam = init_configures()
    smartdashboard = NetworkTables.getTable("SmartDashboard")
    while cam.isOpened():
        _, frame = cam.read()

        frame = cv2.remap(frame, parameters.MAP1, parameters.MAP2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        try:
            distance, angle = detect_hexagon(frame)
            smartdashboard.putNumber("Distance", distance)
            smartdashboard.putNumber("Angle", angle)
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    main()
