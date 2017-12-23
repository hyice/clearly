#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import view


class PreviewFrame(wx.Frame):
    def __init__(self, file_path):
        wx.Frame.__init__(self, None, -1, size=(500, 500))
        view.PreviewPanel(self, file_path)