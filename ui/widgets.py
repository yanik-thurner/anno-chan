import copy
from typing import Callable, Optional

import PySide2
from PIL import Image
from PySide2.QtCore import QPointF, QRectF, QRect
from PySide2.QtGui import QImage, QPaintEvent, QPainter, QCursor, Qt, QPen, QColor, QResizeEvent, QMouseEvent, \
    QWheelEvent
from PySide2.QtWidgets import QWidget, QBoxLayout, QSpacerItem

from dataset import CocoDataset
from helper import pos_in_bbox, points_to_bbox, xyxy_to_xywh


class AnnotationWidget(QWidget):
    def __init__(self, parent: QWidget, categories, category_colors: dict, annotations_changed_callback, annotatable=True):
        super().__init__(parent)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight, self))
        self.layout().addItem(QSpacerItem(0, 0))
        self._placeholder = QWidget(self)
        self._placeholder.setMouseTracking(True)
        self.layout().addWidget(self._placeholder)
        self.layout().addItem(QSpacerItem(0, 0))
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._aspect_ratio: float = 1
        self._categories: list = categories
        self._category_colors: dict = category_colors
        self._annotations_changed_callback: Callable = annotations_changed_callback
        self._annotatable: bool = annotatable
        # last press in drawing coordinates
        self._last_left_press_abs: Optional[tuple] = None
        self._cursor_old_pos_abs: Optional[tuple] = None
        self._image: Optional[QImage] = None
        self.data: Optional[dict] = None
        self.selected_category: Optional[int] = None
        self.score_threshold: float = 0
        self._draw_rect: QRectF = self._placeholder.geometry()

        self.setMouseTracking(True)

    def load_data(self, data: dict, image: QImage):
        self.data = data
        self._image = image
        self._aspect_ratio = image.width()/image.height() if image is not None else 1

        # hack to force a resize event
        self.resize(self.size().width() - 1, self.size().height())
        self.resize(self.size().width() + 1, self.size().height())
        
        self.repaint()

    def resizeEvent(self, event: QResizeEvent):
        if not self.isVisible():
            return

        w = event.size().width()
        h = event.size().height()

        if w / h > self._aspect_ratio:  # too wide
            self.layout().setDirection(QBoxLayout.LeftToRight)
            widget_stretch = h * self._aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 0.5
            self._draw_rect = QRect(int(outer_stretch), 0, int(widget_stretch), h)
        else:  # too tall
            self.layout().setDirection(QBoxLayout.TopToBottom)
            widget_stretch = w / self._aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 0.5
            self._draw_rect = QRect(0, int(outer_stretch), w, int(widget_stretch))

        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)

    def _set_hover_cursor(self, pos_abs):
        if self.data is None:
            return

        index = self._index_of_box_coordinates(self._abs_to_rel_(pos_abs))

        if self._annotatable and self._last_left_press_abs:
            self.repaint()
        elif self._annotatable and index is None:
            self.setCursor(Qt.CrossCursor)
        elif not self._annotatable and index is None:
            self.setCursor(Qt.ArrowCursor)
        elif index is not None:
            self.setCursor(Qt.PointingHandCursor)

    def _move_drawn_rect(self, cursor_new_pos_abs):
        last_middle_press_rel = self._abs_to_rel_(self._cursor_old_pos_abs)
        pos_rel = self._abs_to_rel_(cursor_new_pos_abs)
        diff_rel = (last_middle_press_rel[0] - pos_rel[0], last_middle_press_rel[1] - pos_rel[1])

        self._draw_rect.moveLeft(self._draw_rect.x() - diff_rel[0] * self._draw_rect.width())
        self._draw_rect.moveTop(self._draw_rect.y() - diff_rel[1] * self._draw_rect.height())
        self._move_image_to_borders()

        self._cursor_old_pos_abs = cursor_new_pos_abs
        self.repaint()

    def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent):
        if self._image is None or not self.isVisible():
            return

        pos_abs = (event.pos().x(), event.pos().y())
        if self._cursor_old_pos_abs is None:
            self._set_hover_cursor(pos_abs)
        else:
            self. setCursor(Qt.DragMoveCursor)
            self._move_drawn_rect(pos_abs)

    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent):
        if event.button() is Qt.MouseButton.LeftButton:
            self._last_left_press_abs = (event.pos().x(), event.pos().y())
        if event.button() is Qt.MouseButton.RightButton:
            self._cursor_old_pos_abs = (event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent):
        if self.data is None or not self.isVisible():
            return

        if event.button() is Qt.MouseButton.LeftButton:
            pos_abs = (event.pos().x(), event.pos().y())
            pos_rel = self._abs_to_rel_(pos_abs)
            last_left_press_rel = self._abs_to_rel_(self._last_left_press_abs)
            bbox_rel = points_to_bbox(pos_rel, last_left_press_rel, (1, 1))

            if bbox_rel[2] < 0.002 or bbox_rel[3] < 0.002:
                pos_rel = last_left_press_rel

            click = pos_rel == last_left_press_rel
            if click or not self._annotatable:
                self._change_selections(pos_rel)
            elif not click and self._annotatable and self.selected_category is not None \
                    and bbox_rel[2] > 0.002 and bbox_rel[3] > 0.002:
                self._add_new_annotation(bbox_rel)

            self._last_left_press_abs = None
            self._annotations_changed_callback()
        if event.button() is Qt.MouseButton.RightButton:
            self._cursor_old_pos_abs = None
        self.repaint()

    def _move_image_to_borders(self):
        if self._draw_rect.x() > self._placeholder.x():
            self._draw_rect.moveLeft(self._placeholder.x())
        if self._draw_rect.y() > self._placeholder.y():
            self._draw_rect.moveTop(self._placeholder.y())
        if self._draw_rect.x() + self._draw_rect.width() < self._placeholder.x() + self._placeholder.width():
            self._draw_rect.moveLeft(self._placeholder.x() + self._placeholder.width() - self._draw_rect.width())
        if self._draw_rect.y() + self._draw_rect.height() < self._placeholder.y() + self._placeholder.height():
            self._draw_rect.moveTop(self._placeholder.y() + self._placeholder.height() - self._draw_rect.height())

    def _calc_zoomed_rect(self, scale, rel_pos):
        w_old = self._draw_rect.width()
        h_old = self._draw_rect.height()
        self._draw_rect.setWidth(self._draw_rect.width() * scale)
        self._draw_rect.setHeight(self._draw_rect.height() * scale)

        dw = self._draw_rect.width() - w_old
        dh = self._draw_rect.height() - h_old

        self._draw_rect.moveLeft(round(self._draw_rect.x() - dw * rel_pos[0]))
        self._draw_rect.moveTop(round(self._draw_rect.y() - dh * rel_pos[1]))

        if self._draw_rect.width() < self._placeholder.width() or self._draw_rect.height() < self._placeholder.height():
            self._draw_rect = self._placeholder.geometry()

        if scale < 1:
            self._move_image_to_borders()

    def wheelEvent(self, event:PySide2.QtGui.QWheelEvent):
        if self._image is not None and self.isVisible():
            rel_pos = ((event.x() - self._draw_rect.x()) / self._draw_rect.width(),
                       (event.y() - self._draw_rect.y()) / self._draw_rect.height())

            if rel_pos[0] < 0 or rel_pos[1] < 0 or rel_pos[0] > 1 or rel_pos[1] > 1:
                return

            if event.delta() > 0:
                self._calc_zoomed_rect(1.1, rel_pos)
            else:
                self._calc_zoomed_rect(0.8, rel_pos)

            self.repaint()
            pass

    def _index_of_box_coordinates(self, pos_rel):
        for index, annotation in enumerate(self.data['annotations']):
            if pos_in_bbox(pos_rel, annotation['bbox']):
                return index
        return None

    def _change_selections(self, pos_rel):
        index = self._index_of_box_coordinates(pos_rel)
        if index is not None:
            if self.data['annotations'][index]['category_id'] in self._category_colors.keys():
                self.data['selected'][index] = not self.data['selected'][index]

    def _add_new_annotation(self, bbox_rel):
        annotation = CocoDataset.empty_annotation()
        annotation['bbox'] = bbox_rel
        annotation['category_id'] = self.selected_category
        # to seperate from annotations created by prediction
        annotation['id'] = -1
        CocoDataset.add_annotation(self.data, annotation, score=1)

    def paintEvent(self, event: QPaintEvent):
        if self.data is not None:
            painter = QPainter(self)
            painter.drawImage(self._draw_rect, self._image)
            for i, annotation in enumerate(self.data['annotations']):
                if self.data['scores'][i] < self.score_threshold:
                    continue
                self._paint_annotation(annotation, self.data['selected'][i], painter)

            if self._annotatable and self._last_left_press_abs:
                self._paint_new_annotation(painter)

    def _paint_annotation(self, annotation: dict, selected: bool, painter: QPainter):
        if annotation['category_id'] in self._category_colors.keys():
            color = self._category_colors[annotation['category_id']]
            qcolor = QColor(color)
            qcolor.setAlpha(255 if selected else 100)
            pen = QPen(qcolor, 2)
        else:
            pen = QPen(QColor(255, 0, 0, 255), 2)
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        bbox_xywh_abs = self._rel_to_abs(annotation['bbox'])
        painter.drawRect(*bbox_xywh_abs)

        bbox_cat = [bbox_xywh_abs[0] - 1, bbox_xywh_abs[1] + bbox_xywh_abs[3], bbox_xywh_abs[2] + 2, 6]
        painter.fillRect(*bbox_cat, painter.pen().color())
        font = painter.font()
        font.setPointSize(6)
        painter.setPen(QPen(Qt.black))
        painter.setFont(font)
        text = f'{annotation["category_id"]}'
        painter.drawText(QRectF(bbox_cat[0]+2, bbox_cat[1] - 3, bbox_cat[2], bbox_cat[3]+3), text)

    def _paint_new_annotation(self, painter):
        if self.selected_category is None:
            return
        global_pos = QCursor().pos()
        local_pos = self.mapFromGlobal(global_pos)
        pos_abs = (local_pos.x(), local_pos.y())

        color = self._category_colors[self.selected_category]
        qcolor = QColor(color)
        pen = QPen(qcolor, 2)
        painter.setPen(pen)
        bbox_xywh_abs = points_to_bbox(pos_abs, self._last_left_press_abs, (self.width(), self.height()))
        painter.drawRect(*bbox_xywh_abs)

    def _abs_to_rel_(self, bbox_abs: tuple) -> tuple:
        bbox_rel = []

        for i, coordinate in enumerate(bbox_abs):
            relc = coordinate - (self._draw_rect.x() if i == 0 else (self._draw_rect.y() if i == 1 else 0))
            relc = relc / (self._draw_rect.width() if i % 2 == 0 else self._draw_rect.height())
            bbox_rel.append(relc)

        return tuple(bbox_rel)

    def _rel_to_abs(self, bbox_rel: tuple) -> tuple:
        """

        :param bbox_rel: [x, y, w, h] or [x, y]
        :return:
        """
        scale = (self._draw_rect.width(), self._draw_rect.height())
        bbox_abs = []

        for i, coordinate in enumerate(bbox_rel):
            absc = coordinate * (scale[0] if i % 2 == 0 else scale[1])
            absc = absc + (self._draw_rect.x() if i == 0 else (self._draw_rect.y() if i == 1 else 0))
            bbox_abs.append(absc)

        return tuple(bbox_abs)
