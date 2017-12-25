#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import cv2
import view
import numpy as np


class PreviewPanel(wx.Panel):
    def __init__(self, parent, image_path):
        wx.Panel.__init__(self, parent)
        self._init_views()
        self._bind_events()

        self._image_helper = ImageHelper(image_path)
        self._update_bitmap()

    # -----------------------------------
    # 图片缩放

    def _full_fill_scale(self):
        view_size = self.GetSize()
        image_size = self._image_helper.image_size

        width_scale = view_size.width * 1.0 / image_size.width
        height_scale = view_size.height * 1.0 / image_size.height

        return min(width_scale, height_scale)

    def _update_bitmap(self, scale=None):
        if not scale:
            scale = self._full_fill_scale()

        self._image_helper.scale = scale

        view_size = self.GetSize()
        image_size = self._image_helper.scaled_image_size

        display_size = wx.Size(min(view_size.width, image_size.width), min(view_size.height, image_size.height))

        position = wx.Point(
            (view_size.width - display_size.width) / 2.0,
            (view_size.height - display_size.height) / 2.0
        )

        self._image_helper.display_size = display_size
        self._bitmap.image = self._image_helper.wx_image
        self._bitmap.SetSize(display_size)
        self._bitmap.SetPosition(position)

        self.Layout()

    # -----------------------------------
    #  初始化

    def _init_views(self):
        self._bitmap = view.StaticBitmap(self)

    def _bind_events(self):
        self.Bind(wx.EVT_SIZE, self._on_size_change)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_scale_change)

    def _on_size_change(self, event):
        self._update_bitmap()
        event.Skip()

    def _on_scale_change(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            scale = self._image_helper.scale * 1.25
        else:
            scale = self._image_helper.scale * 0.8

        self._update_bitmap(scale)

        event.Skip()


class ImageHelper(object):
    def __init__(self, image_path):
        self.__image_path = image_path

        cv_image = cv2.imdecode(np.fromfile(self.__image_path, dtype=np.uint8), -1)
        self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        self._scale = None
        self._display_size = None

    # -----------------------------------
    # 尺寸数据

    @property
    def image_size(self):
        shape = self._cv_rgb_image.shape
        return wx.Size(shape[1], shape[0])

    @property
    def scaled_image_size(self):
        shape = self._cv_rgb_image.shape
        width = int(shape[1] * (self.scale or 1))
        height = int(shape[0] * (self.scale or 1))
        return wx.Size(width, height)

    # -----------------------------------
    # 图片展示

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        if self._scale == scale:
            return

        self._scale = scale

    @property
    def display_size(self):
        return self._display_size

    @display_size.setter
    def display_size(self, value):
        self._display_size = value

    @property
    def wx_image(self):
        center_x = self.image_size.width / 2.0
        center_y = self.image_size.height / 2.0
        x_min = int(center_x - self._display_size.width / self.scale / 2.0)
        x_max = int(center_x + self._display_size.width / self.scale / 2.0)
        y_min = int(center_y - self._display_size.height / self.scale / 2.0)
        y_max = int(center_y + self._display_size.height / self.scale / 2.0)

        cv_image_to_scale = self._cv_rgb_image[y_min:y_max, x_min:x_max]
        scaled_image = cv2.resize(cv_image_to_scale, (self.display_size.width, self.display_size.height))

        wx_image = wx.Image(self.display_size.width, self.display_size.height)
        image_data = scaled_image.tostring()
        wx_image.SetData(image_data)
        return wx_image
