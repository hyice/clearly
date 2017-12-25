#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import view


class PreviewFrame(wx.Frame):
    def __init__(self, file_path):
        wx.Frame.__init__(self, None, -1, size=(500, 500))
        self.view = view.PreviewPanel(self, file_path)

        self._bind_events()

    def Show(self, show=True):
        super(PreviewFrame, self).Show(show)
        self.Maximize()

    # ----------------------------------------
    # 事件绑定

    def _bind_events(self):
        self.view.Bind(wx.EVT_KEY_DOWN, self._handle_key_press)

    def _handle_key_press(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:  # ESC 键退出程序
            self.Close()

        event.Skip()