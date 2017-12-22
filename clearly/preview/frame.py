#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import view


class PreviewFrame(wx.Frame):
    def __init__(self, file_path):
        wx.Frame.__init__(self, None, -1, size=(500, 500))
        self._init_views()

        image = wx.Image(file_path, wx.BITMAP_TYPE_ANY)
        self.bitmap.update_image(image)

        self.Bind(wx.EVT_MOUSEWHEEL, self._on_scale_change)

    def _on_scale_change(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            scale = self.bitmap.scale_value * 1.25
        else:
            scale = self.bitmap.scale_value * 0.8

        print(scale)
        self.bitmap.scale(scale)

        event.Skip()

    def _init_views(self):
        panel = wx.Panel(self)

        self.bitmap = view.StaticBitmap(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, -1, wx.EXPAND)
        panel.SetSizer(sizer)