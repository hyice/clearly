#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class StaticBitmap(wx.StaticBitmap):
    def __init__(self, *args, **kwargs):
        wx.StaticBitmap.__init__(self,*args, **kwargs)

        self._image = None

    @property
    def image(self) -> wx.Image:
        return self._image

    @image.setter
    def image(self, image: wx.Image):
        self._image = image
        bitmap = self._image.ConvertToBitmap()
        self.SetBitmap(bitmap)
