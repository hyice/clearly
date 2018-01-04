#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import math


class CVImage(object):
    def __init__(self, file_path):
        self._file_path = file_path

        self._cv_rgb_image = None
        self.reload()

    @property
    def image(self):
        return self._cv_rgb_image

    @property
    def size(self):
        shape = self._cv_rgb_image.shape
        return shape[1], shape[0]

    # -----------------------------
    # 保存与加载

    def save(self):
        ext = os.path.splitext(self._file_path)[1]
        image = cv2.cvtColor(self._cv_rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imencode(ext, image)[1].tofile(self._file_path)

    def reload(self):
        cv_image = cv2.imdecode(np.fromfile(self._file_path, dtype=np.uint8), -1)
        self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

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

    def auto_make_whiter(self):
        self.compensate_light()

        hist = cv2.calcHist([self._cv_rgb_image], [0], None, [256], [0, 255])
        _, max_val, _, max_loc = cv2.minMaxLoc(hist)

        index = 255
        for index in range(int(max_loc[1]), 0, -1):
            intensity = hist[index][0]
            rate = intensity / max_val
            if rate < 0.05:
                break

        gray_image = cv2.cvtColor(self._cv_rgb_image, cv2.COLOR_RGB2GRAY)
        gray_image[gray_image > index] = 255
        self._cv_rgb_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)

    def reverse_color(self):
        self._cv_rgb_image = 255 - self._cv_rgb_image

    def compensate_light(self):
        gray_image = cv2.cvtColor(self._cv_rgb_image, cv2.COLOR_RGB2GRAY)

        image_row_count, image_col_count = gray_image.shape
        average = np.mean(gray_image)

        block_size = 50
        block_row_count = int(math.ceil(image_row_count * 1.0 / block_size))
        block_col_count = int(math.ceil(image_col_count * 1.0 / block_size))
        block_gray_array = np.zeros((block_row_count, block_col_count))
        for i in range(0, block_row_count):
            min_row_index = i * block_size
            max_row_index = (i + 1) * block_size
            max_row_index = max_row_index if max_row_index < image_row_count else image_row_count

            for j in range(0, block_col_count):
                min_col_index = j * block_size
                max_col_index = (j + 1) * block_size
                max_col_index = max_col_index if max_col_index < image_col_count else image_col_count

                block_gray_array[i, j] = np.mean(gray_image[min_row_index:max_row_index, min_col_index:max_col_index])

        gray_gap_array = cv2.resize(block_gray_array - average, (image_col_count, image_row_count),
                                    interpolation=cv2.INTER_CUBIC)
        compensated_image = gray_image - gray_gap_array
        compensated_image = compensated_image.astype(np.uint8)

        self._cv_rgb_image = cv2.cvtColor(compensated_image, cv2.COLOR_GRAY2RGB)

    def hist(self):
        hist = cv2.calcHist([self._cv_rgb_image], [0], None, [256], [0, 255])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(hist)
        hist_img = np.zeros([256, 256, 3], np.uint8)
        hpt = int(0.9 * 256)

        for h in range(256):
            intensity = int(hist[h] * hpt / max_val)
            cv2.line(hist_img, (h, 256), (h, 256 - intensity), [255, 255, 255])

        return hist_img



