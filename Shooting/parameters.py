import numpy as np

CAMERA_MATRIX = np.array([[4.69383922e+03, 0.00000000e+00, 9.36476511e+02],
                            [0.00000000e+00, 4.77948268e+03, 5.02461779e+02],
                            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST_COEFS = np.array([[-7.87178803e-01,  3.25448997e+00,  1.02606369e-02, -1.47615590e-02,
                        -2.68854364e+02]])

# ------------------------------------------------- Fill ------------------------------------------------- #
MIN_HSV = (0, 0, 80)
MAX_HSV = (179, 226, 142)

IMAGE_HEIGHT = 240
IMAGE_WIDTH = 320

PIXEL_TO_DEGREES_RATIO_Y = 5
PIXEL_TO_DEGREES_RATIO_X = 5.3

FOCAL_LENGTH = 754.71 # mm

HEXAGON_WIDTH = 530 # mm