#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import view
import image


class PreviewFrame(wx.Frame):
    def __init__(self, file_path):
        wx.Frame.__init__(self, None, -1, size=(500, 500))

        self.cv_image = image.CVImage(file_path)
        self.view = view.PreviewPanel(self)
        self.view.update_image(self.cv_image.image)

        self._is_modified = False

        self._init_right_click_menu()

        self._bind_events()

    def Show(self, show=True):
        super(PreviewFrame, self).Show(show)
        self.Maximize()

    # ----------------------------------------
    # 菜单

    def _init_right_click_menu(self):
        menu = view.Menu()
        menu.append_item('向左旋转', self._rotate_image)
        menu.append_item('向右旋转', self._rotate_image, True)

        menu.append_separator()
        menu.append_item('裁剪', self._crop_image)

        self._right_click_menu = menu

    def _rotate_image(self, clockwise=False):
        self._is_modified = True

        self.cv_image.rotate(clockwise)
        self.view.update_image(self.cv_image.image)

    def _crop_image(self):
        self._is_modified = True

        selection_rect = self.view.selection_area()
        self.cv_image.crop(selection_rect)
        self.view.update_image(self.cv_image.image)

    # ----------------------------------------
    # 退出并保存

    def _exit(self):
        if not self._is_modified:
            self.Close()
            return

        result = self._show_save_confirm_dialog()

        if result == wx.ID_CANCEL:
            return

        if result == wx.ID_YES:
            self._save()

        self.Close()

    def _save(self):
        self.cv_image.save()

    def _show_save_confirm_dialog(self):
        dialog = wx.MessageDialog(self, '要保存对此图像的修改吗？', '提示', wx.YES_NO | wx.CANCEL)
        dialog.SetYesNoCancelLabels('保存', '不保存', '取消')

        result = dialog.ShowModal()
        dialog.Destroy()

        return result

    # ----------------------------------------
    # 事件绑定

    def _bind_events(self):
        self.view.Bind(wx.EVT_KEY_DOWN, self._handle_key_press)

        self.view.Bind(wx.EVT_RIGHT_DOWN, self._on_right_mouse_down)

    def _handle_key_press(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:  # ESC 键退出程序
            self._exit()

        event.Skip()

    def _on_right_mouse_down(self, event):
        self.view.PopupMenu(self._right_click_menu, event.GetPosition())
        event.Skip()