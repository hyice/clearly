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

        self._scale = 1.0

        self._image_helper = ImageHelper(image_path)
        self.scale = self._full_fill_scale()

    # -----------------------------------
    # 图片缩放
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._bitmap.image = self._image_helper.image_with_scale(self._scale)
        self._reposition_bitmap()

    def _full_fill_scale(self):
        view_size = self.GetSize()
        image_size = self._image_helper.image.GetSize()

        width_scale = view_size.width * 1.0 / image_size.width
        height_scale = view_size.height * 1.0 / image_size.height

        return min(width_scale, height_scale)

    def _reposition_bitmap(self):
        view_size = self.GetSize()
        image_size = self._bitmap.image.GetSize()

        position = wx.Point(
            (view_size.Width - image_size.Width) / 2.0,
            (view_size.Height - image_size.Height) / 2.0
        )

        self._bitmap.SetSize(image_size)
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
        self.scale = self._full_fill_scale()
        event.Skip()

    def _on_scale_change(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            self.scale = self.scale * 1.25
        else:
            self.scale = self.scale * 0.8

        event.Skip()


class ImageHelper(object):
    def __init__(self, image_path):
        self._image_path = image_path

        self._image = None
        self._cv_rgb_image = None

    # -----------------------------------
    #  读取图片

    @property
    def cv_rgb_image(self):
        if self._cv_rgb_image is None:
            cv_image = cv2.imdecode(np.fromfile(self._image_path, dtype=np.uint8), -1)
            self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        return self._cv_rgb_image

    @property
    def image(self):
        return self.image_with_scale(1.0)

    def image_with_scale(self, scale):
        shape = self.cv_rgb_image.shape
        width = int(shape[1] * scale)
        height = int(shape[0] * scale)

        scaled = cv2.resize(self.cv_rgb_image, (width, height))

        wx_image = wx.Image(width, height)
        image_data = scaled.tostring()
        wx_image.SetData(image_data)
        return wx_image
