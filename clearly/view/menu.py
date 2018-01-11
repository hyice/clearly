#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class Menu(wx.Menu):
    def __init__(self, *args, **kwargs):
        wx.Menu.__init__(self, *args, **kwargs)

        self.handlers = {}
        self.params = {}
        self._sub_menus = set()

        self.Bind(wx.EVT_MENU, self._on_menu_clicked)

    def append_item(self, title, handler, *args):
        item_id = wx.NewId()
        self.handlers[item_id] = handler
        self.params[item_id] = args

        return self.Append(item_id, title)

    def append_separator(self):
        self.AppendSeparator()

    def append_sub_menu(self, title, sub_menu):
        self._sub_menus.add(sub_menu)
        self.Append(wx.ID_ANY, title, sub_menu)

    def _on_menu_clicked(self, event):
        item_id = event.GetId()
        self.handle_menu_item_click(item_id)
        event.Skip()

    def handle_menu_item_click(self, item_id):
        try:
            handler = self.handlers[item_id]
            params = self.params[item_id]
            handler(*params)
            return True
        except KeyError:
            pass

        for sub_menu in self._sub_menus:
            if sub_menu.handle_menu_item_click(item_id):
                return True
        return False
