#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class StaticBitmap(wx.StaticBitmap):
    def __init__(self, parent):
        wx.StaticBitmap.__init__(self, parent)

    # ---------------------------------------------------
    # 更新图片

    def update_image(self, image):
        """ 更新图片, 自动调整图片尺寸以适应窗口大小
        :type image: wx.Image
        """
        bitmap = image.ConvertToBitmap()
        self.SetBitmap(bitmap)

