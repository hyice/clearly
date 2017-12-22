#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class StaticBitmap(wx.StaticBitmap):
    def __init__(self, parent):
        wx.StaticBitmap.__init__(self, parent)
        self._image = None
        self._scale = 1.0
        self._best_size = None
        self._is_scaling = False

        self.Bind(wx.EVT_SIZE, self._size_changed)

    # ---------------------------------------------------
    # 更新图片

    def update_image(self, image):
        """ 更新图片, 自动调整图片尺寸以适应窗口大小
        :type image: wx.Image
        """
        self._image = image
        self._best_size = None

        self._resize_and_set_bitmap()

    def _size_changed(self, event):
        self._best_size = None
        self._resize_and_set_bitmap()
        event.Skip()

    def _resize_and_set_bitmap(self):
        if not self._image:
            return

        size = self._best_size_for_image()
        bitmap = self._image.Scale(size.width*self.scale_value, size.height*self.scale_value).ConvertToBitmap()
        bitmap.SetSize(self.GetSize())
        self.SetBitmap(bitmap)

    def _best_size_for_image(self):
        """ 在保持图片比例的情况下，计算图片的最大填充尺寸
        :return image size
        :rtype wx.Size
        """

        if self._best_size:
            return self._best_size

        view_size = self.GetSize()
        image_size = self._image.GetSize()

        width_ratio = view_size.width * 1.0 / image_size.width
        height_ratio = view_size.height * 1.0 / image_size.height

        if width_ratio > height_ratio:
            new_width = image_size.width * height_ratio
            new_height = view_size.height
        else:
            new_width = view_size.width
            new_height = image_size.height * width_ratio

        self._best_size = wx.Size(width=new_width, height=new_height)
        return self._best_size

    # -----------------------------------------------
    # 图片缩放

    @property
    def scale_value(self):
        return self._scale

    def scale(self, scale):
        if scale > 10 or scale < 0.1:
            return

        self._scale = scale
        self._resize_and_set_bitmap()

