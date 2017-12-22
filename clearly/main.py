#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import preview
import os


def show_file_chooser(parent=None, title=u'选择文件', wildcard="*"):
    dialog = wx.FileDialog(parent, title, os.getcwd(), style=wx.FD_OPEN, wildcard=wildcard)
    result = dialog.ShowModal()
    file_path = None
    if result == wx.ID_OK:
        file_path = dialog.GetPath()
    dialog.Destroy()
    return file_path


def main():
    app = wx.App()

    path = show_file_chooser()
    if path:
        preview.PreviewFrame(path).Show()

    app.MainLoop()


if __name__ == '__main__':
    main()