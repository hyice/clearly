#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class ImagePrintout(wx.Printout):
    def __init__(self, image):
        wx.Printout.__init__(self)

        self._image = image
        self._bitmap = None

    def HasPage(self, page_num):
        return page_num == 1

    def OnPreparePrinting(self):
        dc = self.GetDC()
        dc_width, dc_height = dc.GetSize()
        image_height, image_width, _ = self._image.shape

        width_scale = dc_width / image_width
        height_scale = dc_height / image_height

        full_fill_scale = min(width_scale, height_scale)

        width_scale_after_rotate = dc_width / image_height
        height_scale_after_rotate = dc_height / image_width
        full_fill_scale_after_rotate = min(width_scale_after_rotate, height_scale_after_rotate)

        wx_image = wx.Image(image_width, image_height)
        image_data = self._image.tostring()
        wx_image.SetData(image_data)

        if full_fill_scale_after_rotate > full_fill_scale:
            wx_image = wx_image.Rotate90().Scale(image_height * full_fill_scale_after_rotate,
                                                 image_width * full_fill_scale_after_rotate)
        else:
            wx_image = wx_image.Scale(image_width * full_fill_scale, image_height * full_fill_scale)

        self._bitmap = wx_image.ConvertToBitmap()

    def OnPrintPage(self, pageNum):
        dc = self.GetDC()

        dc.SetPen(wx.Pen('black', 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dc.DrawBitmap(self._bitmap, 0, 0)
        return True
