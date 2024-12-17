#!/usr/bin/env python

from calibration import calibrate_camera
from homography import apply_homography

CHECKERBOARD_DIMS = (27, 17)
IMAGES_PATH = './images/*.png'
IMAGE_PATH = './images/checkerboard-pattern-on-desk.png'

if __name__ == "__main__":
    mtx, dist = calibrate_camera(IMAGES_PATH, CHECKERBOARD_DIMS)
    apply_homography(IMAGE_PATH, mtx, dist, CHECKERBOARD_DIMS)