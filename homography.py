#!/usr/bin/env python

import cv2
import numpy as np

def apply_homography(image_path, mtx, dist, checkerboard_dims):
    CHECKERBOARD = checkerboard_dims
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    img = cv2.imread(image_path)
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    h, w = undistorted_img.shape[:2]

    gray = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        src_pts_rect = np.float32([
            corners[0][0],
            corners[CHECKERBOARD[0] - 1][0],
            corners[-1][0],
            corners[-CHECKERBOARD[0]][0]
        ])
        dst_pts = np.float32([
            corners[0][0],
            [corners[CHECKERBOARD[0] - 1][0][0], corners[0][0][1]],
            [corners[CHECKERBOARD[0] - 1][0][0], corners[-1][0][1]],
            [corners[0][0][0], corners[-1][0][1]]
        ])
        H, _ = cv2.findHomography(src_pts_rect, dst_pts)
        output_size = (w, h)
        warped_img = cv2.warpPerspective(undistorted_img, H, output_size)
        cv2.imwrite("aligned_image.png", warped_img)
        cv2.imshow("Aligned Image", warped_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Checkerboard corners not found in the image!")