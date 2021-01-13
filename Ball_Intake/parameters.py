import numpy as np

PIXEL_TO_DEGREES_RATIO = 6.25

# image width in px
IMAGE_WIDTH = 320

# image height in px
IMAGE_HEIGHT = 240

# parameters after running the camera_calibration code
CAMERA_MATRIX = np.array([[676.89754647, 0.0, 321.02857627],
                          [0.0, 675.87782307, 242.78043906],
                          [0.0, 0.0, 1.0]])
DIST_COEFS = np.array([1.24045728e-01, -8.43313568e-01, -6.88290997e-04, 2.84287667e-03, 1.26710943e+00])

# target values for inRange function
MIN_HSV = (0, 0, 80)
MAX_HSV = (179, 226, 142)


FOCAL_LENGTH = 320  # mm
LIGHT_REFLECTOR_WIDTH = 50  # mm
LIGHT_REFLECTOR_HEIGHT = 140  # mm
LIGHT_REFLECTOR_WIDTH_PX = 16  # mm
LIGHT_REFLECTOR_HEIGHT_PX = None