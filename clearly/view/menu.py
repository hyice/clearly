#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class Menu(wx.Menu):
    def __init__(self, *args, **kwargs):
        wx.Menu.__init__(self, *args, **kwargs)

        self._handlers = {}
        self._params = {}

        self.Bind(wx.EVT_MENU, self._on_menu_clicked)

    def append(self, title, handler, *args):
        item_id = wx.NewId()
        self._handlers[item_id] = handler
        self._params[item_id] = args

        self.Append(item_id, title)

    def _on_menu_clicked(self, event):
        item_id = event.GetId()
        handler = self._handlers[item_id]
        params = self._params[item_id]
        handler(*params)
        event.Skip()