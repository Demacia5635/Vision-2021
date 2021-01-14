import json
import sys

import cv2
import ntcore
import numpy as np
from networktables import NetworkTables, NetworkTablesInstance
from cscore import CameraServer

from configs import Vision
from find_ball import detect_ball


if __name__ == "__main__":
    # Create a class containing all the information the raspberry needs
    vision = []
    if len(sys.argv) >= 2:
        vision = Vision(sys.argv[1])
    else:
        vision = Vision()

    # read configuration
    if not vision.config_was_read:
        sys.exit(1)

    # start NetworkTables
    ntinst = NetworkTablesInstance.getDefault()
    if server:
        print("Setting up NetworkTables server")
        ntinst.startServer()
    else:
        print("Setting up NetworkTables client for team {}".format(vision.team))
        ntinst.startClientTeam(vision.team)

    cap = CameraServer.getInstance().getVideo()
    NetworkTables.initialize(server='10.56.36.2')

    sd = NetworkTables.getTable('SmartDashboard')
    # loop forever
    frame = np.ones((160, 120, 3))
    while True:
        _, frame = cap.grabFrame(frame)
        frame = frame.astype('uint8')
        data = detect_ball(frame)
        last_ang = sd.getNumber("BallAngle", 0)
        last_dis = sd.getNumber("BallDistance", 0)
        if data is None:
            data = {
                "distance": 0,
                "angle": 0
            }
        if last_dis != data["distance"]:
            sd.putNumber('BallDistance', data["distance"])
        if last_ang != data["angle"]:
            sd.putNumber('BallAngle', data["angle"])
