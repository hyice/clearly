#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os


class CVImage(object):
    def __init__(self, file_path):
        self._file_path = file_path

        cv_image = cv2.imdecode(np.fromfile(self._file_path, dtype=np.uint8), -1)
        self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    @property
    def image(self):
        return self._cv_rgb_image

    @property
    def size(self):
        shape = self._cv_rgb_image.shape
        return shape[1], shape[0]

    # -----------------------------
    # 保存

    def save(self):
        ext = os.path.splitext(self._file_path)[1]
        cv2.imencode(ext, self._cv_rgb_image)[1].tofile(self._file_path)

    # -----------------------------
    # 旋转、裁剪、清除区域内容等基本操作

    def rotate(self, clockwise=False):
        if clockwise:
            rotate_code = cv2.ROTATE_90_CLOCKWISE
        else:
            rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE

        self._cv_rgb_image = cv2.rotate(self._cv_rgb_image, rotateCode=rotate_code)

    def crop(self, rect):
        x_min, y_min, x_max, y_max = self.valid_operation_rect(rect)
        self._cv_rgb_image = self._cv_rgb_image[y_min:y_max, x_min:x_max]

    def clear(self, rect):
        x_min, y_min, x_max, y_max = self.valid_operation_rect(rect)
        self._cv_rgb_image[y_min:y_max, x_min:x_max] = 255

    def valid_operation_rect(self, rect):
        x, y, width, height = rect
        image_width, image_height = self.size

        x_min = max(0, x)
        y_min = max(0, y)
        x_max = min(image_width, x + width)
        y_max = min(image_height, y + height)
        return x_min, y_min, x_max, y_max

    # ---------------------------------------------
    # 图片颜色相关操作

    def reverse_color(self):
        self._cv_rgb_image = 255 - self._cv_rgb_image



