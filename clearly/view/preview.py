#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import cv2
import view
import numpy as np


class PreviewPanel(wx.Panel):
    def __init__(self, parent, image_path):
        wx.Panel.__init__(self, parent)

        self._init_views()
        self._bind_events()

        self._last_drag_point = None
        self._is_moving = False

        self._is_selecting = False
        self._selecting_start_point = None
        self._selection_view = DashRect(self, size=(0, 0))
        self._selection_view.Disable()

        self._image_helper = ImageHelper(image_path)
        self._update_bitmap()

    # -----------------------------------
    # 图片缩放

    def _scale_image(self, larger=True):
        if larger:
            scale = self._image_helper.scale * 1.25
        else:
            scale = self._image_helper.scale * 0.8

        self._update_bitmap(scale)

    def _full_fill_scale(self):
        view_size = self.GetSize()
        image_size = self._image_helper.image_size

        width_scale = view_size.width * 1.0 / image_size.width
        height_scale = view_size.height * 1.0 / image_size.height

        return min(width_scale, height_scale)

    def _update_bitmap(self, scale=None):
        if not scale:
            scale = self._full_fill_scale()

        self._image_helper.scale = scale

        view_size = self.GetSize()
        image_size = self._image_helper.scaled_image_size

        display_size = wx.Size(min(view_size.width, image_size.width), min(view_size.height, image_size.height))

        position = wx.Point(
            (view_size.width - display_size.width) / 2.0,
            (view_size.height - display_size.height) / 2.0
        )

        self._image_helper.display_size = display_size
        self._bitmap.image = self._image_helper.wx_image
        self._bitmap.SetSize(display_size)
        self._bitmap.SetPosition(position)

        self.Layout()

    # -----------------------------------
    # 图片平移

    def _start_moving(self, point):
        self._is_moving = True
        self._last_drag_point = point

    def _moving_to(self, point):
        dx, dy = point - self._last_drag_point
        x_unit = self.GetSize().width >> 7
        y_unit = self.GetSize().height >> 7
        if abs(dx) < x_unit and abs(dy) < y_unit:
            return

        ori_offset = self._image_helper.offset
        self._image_helper.offset = (self._image_helper.offset[0] - dx, self._image_helper.offset[1] - dy)
        self._last_drag_point = point

        if ori_offset != self._image_helper.offset:
            self._update_bitmap(self._image_helper.scale)

    def _end_moving(self, point):
        self._moving_to(point)
        self._last_drag_point = None
        self._is_moving = False

    # ------------------------------------
    # 选择区域

    def _start_selecting(self, point):
        point = self._valid_selecting_point(point)

        self._is_selecting = True
        self._selecting_start_point = point

        self._selection_view.SetRect((point.x, point.y, 0, 0))
        self._selection_view.Show()

    def _selecting_to(self, point):
        point = self._valid_selecting_point(point)

        x = min(point.x, self._selecting_start_point.x)
        width = abs(point.x - self._selecting_start_point.x)
        y = min(point.y, self._selecting_start_point.y)
        height = abs(point.y - self._selecting_start_point.y)

        self._selection_view.SetRect((x, y, width, height))

    def _end_selecting(self, point):
        point = self._valid_selecting_point(point)

        self._selecting_to(point)
        self._selection_view.start_animation()
        self._is_selecting = False

    def _hide_selection(self):
        self._selection_view.stop_animation()
        self._selection_view.Hide()

    def _valid_selecting_point(self, point):
        x, y = point
        x_min, y_min, width, height = self._bitmap.GetRect()
        x_max = x_min + width
        y_max = y_min + height

        x = min(x_max, max(x, x_min))
        y = min(y_max, max(y, y_min))

        return wx.Point(x, y)

    # -----------------------------------
    #  初始化

    def _init_views(self):
        self._bitmap = view.StaticBitmap(self)
        self._bitmap.Disable()

    def _bind_events(self):
        self.Bind(wx.EVT_SIZE, self._on_size_change)

        self.Bind(wx.EVT_MOUSEWHEEL, self._on_scale_change)

        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_mouse_down)
        self.Bind(wx.EVT_MOTION, self._on_mouse_move)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_mouse_up)

    def _on_size_change(self, event):
        self._update_bitmap()
        event.Skip()

    def _on_scale_change(self, event):
        rotation = event.GetWheelRotation()
        self._scale_image(rotation > 0)
        self._hide_selection()
        event.Skip()

    def _on_left_mouse_down(self, event):
        is_control_down = event.ControlDown()
        self._hide_selection()
        if is_control_down:
            self._start_selecting(event.GetPosition())
        else:
            self._start_moving(event.GetPosition())
        event.Skip()

    def _on_mouse_move(self, event):
        if self._is_moving:
            self._moving_to(event.GetPosition())

        if self._is_selecting:
            self._selecting_to(event.GetPosition())

        event.Skip()

    def _on_left_mouse_up(self, event):
        if self._is_moving:
            self._end_moving(event.GetPosition())

        if self._is_selecting:
            self._end_selecting(event.GetPosition())

        event.Skip()


class ImageHelper(object):
    def __init__(self, image_path):
        self.__image_path = image_path

        cv_image = cv2.imdecode(np.fromfile(self.__image_path, dtype=np.uint8), -1)
        self._cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        self._scale = None
        self._display_size = wx.Size(0, 0)
        self._offset = (0, 0)

    # -----------------------------------
    # 尺寸数据

    @property
    def image_size(self):
        shape = self._cv_rgb_image.shape
        return wx.Size(shape[1], shape[0])

    @property
    def scaled_image_size(self):
        shape = self._cv_rgb_image.shape
        width = int(shape[1] * self.scale)
        height = int(shape[0] * self.scale)
        return wx.Size(width, height)

    # -----------------------------------
    # 图片展示

    @property
    def scale(self):
        return self._scale or 1.0

    @scale.setter
    def scale(self, scale):
        if self._scale == scale:
            return
        ori_scale = self.scale
        self._scale = scale

        self.offset = (self.offset[0] / ori_scale * scale, self.offset[1] / ori_scale * scale)

    @property
    def display_size(self):
        return self._display_size

    @display_size.setter
    def display_size(self, value):
        self._display_size = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        if value == self._offset:
            return

        dx, dy = value
        image_size = self.scaled_image_size
        width_gap = (image_size.width - self.display_size.width) / 2.0
        if width_gap <= 0:
            dx = 0
        elif dx + width_gap < 0:
            dx = -width_gap
        elif dx - width_gap > 0:
            dx = width_gap

        height_gap = (image_size.height - self.display_size.height) / 2.0
        if height_gap <= 0:
            dy = 0
        elif dy + height_gap < 0:
            dy = -height_gap
        elif dy - height_gap > 0:
            dy = height_gap

        self._offset = (dx, dy)

    @property
    def wx_image(self):
        center_x = self.image_size.width / 2.0 + self.offset[0] / self.scale
        center_y = self.image_size.height / 2.0 + self.offset[1] / self.scale
        x_min = int(center_x - self._display_size.width / self.scale / 2.0)
        x_max = int(center_x + self._display_size.width / self.scale / 2.0)
        y_min = int(center_y - self._display_size.height / self.scale / 2.0)
        y_max = int(center_y + self._display_size.height / self.scale / 2.0)

        cv_image_to_scale = self._cv_rgb_image[y_min:y_max, x_min:x_max]
        scaled_image = cv2.resize(cv_image_to_scale, (self.display_size.width, self.display_size.height))

        wx_image = wx.Image(self.display_size.width, self.display_size.height)
        image_data = scaled_image.tostring()
        wx_image.SetData(image_data)
        return wx_image


class DashRect(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, style=wx.TRANSPARENT_WINDOW, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self._on_paint)

        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self._timer)

        self._black_dash = True

    def start_animation(self):
        self._timer.Start(800)

    def stop_animation(self):
        self._timer.Stop()

    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        self._draw(dc)

    def _on_timer(self, event):
        dc = wx.ClientDC(self)
        self._draw(dc)

    def _draw(self, dc):
        solid_pen = wx.Pen('#4c4c4c' if self._black_dash else '#ffffff', 1, wx.SOLID)

        dash_pen = wx.Pen('#ffffff' if self._black_dash else '#4c4c4c', 1, wx.USER_DASH)
        dash_pen.SetDashes([6, 8])

        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dc.SetPen(solid_pen)
        dc.DrawRectangle((0, 0), self.GetSize())

        dc.SetPen(dash_pen)
        dc.DrawRectangle((0, 0), self.GetSize())

        self._black_dash = not self._black_dash
