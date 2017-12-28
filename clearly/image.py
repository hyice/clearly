#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class CVImage(object):
    def __init__(self, file_path):
        self._file_path = file_path

        cv_image = cv2.imdecode(np.fromfile(self._file_path, dtype=np.uint8), -1)
        self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    @property
    def image(self):
        return self._cv_rgb_image

    # -----------------------------
    # 旋转

    def rotate(self, clockwise=False):
        if clockwise:
            rotate_code = cv2.ROTATE_90_CLOCKWISE
        else:
            rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE

        self._cv_rgb_image = cv2.rotate(self._cv_rgb_image, rotateCode=rotate_code)




