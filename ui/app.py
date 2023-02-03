import copy
import glob
import os
import sys
from typing import Optional

import randomcolor
import torch
from PIL.ImageQt import ImageQt
from PySide2 import QtCore
from PySide2.QtCore import QMetaMethod, Qt, QEvent
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QMessageBox

from dataset import CocoDataset
from helper import Reference
from ui.mainui import Ui_MainWindow
from ui.widgets import AnnotationWidget
from framework import AnnotationFramework


# pyside2-uic ui/main.ui > ui/mainui.py
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._framework = AnnotationFramework(root_path, annotation_file_path, SAVE_RATE, self.ui.slider_score.value()/100)
        self._annotation_widget_old: Optional[AnnotationWidget] = None
        self._annotation_widget_pred: Optional[AnnotationWidget] = None
        self._annotation_widget_new: Optional[AnnotationWidget] = None
        self._category_colors: dict = {}
        self._score_threshold: float = 0

        self._init_predictor()
        self._init_annotation_widgets()
        if self._framework.categories is not None:
            self.init_categories()
        else:
            self.ui.button_next.setDisabled(True)

        self.score_threshold_changed()
        self._connect_slots()
        self.installEventFilter(self)

    def _init_predictor(self):
        models = [os.path.basename(x) for x in glob.glob(os.path.join('./models', '*.pth'))]
        self.ui.combobox_models.addItems(models)
        selected_model = self.ui.combobox_models.itemText(self.ui.combobox_models.currentIndex())
        self._framework.init_predictor(os.path.join('./models', selected_model))

    def _new_category_button(self, category, parent):
        b = QPushButton(f'{category["id"]}: {category["name"]}', parent)
        b.setObjectName(str(category["id"]))
        b.category_index = category['id']
        b.setGeometry(0, 0, 100, 20)
        b.clicked.connect(self.select_category)
        b.setStyleSheet(f'color: {self._category_colors[category["id"]]}')
        b.setFocusPolicy(Qt.NoFocus)
        return b

    def _new_remove_category_button(self, category, index, parent):
        remove = QPushButton('-', parent)
        remove.button_index = index
        remove.category_index = category["id"]
        remove.setMaximumSize(20, 20)
        remove.clicked.connect(self.remove_category)
        remove.setFocusPolicy(Qt.NoFocus)
        return remove

    def init_categories(self):
        categories = self._framework.categories
        for i in range(self.ui.target_categories.layout().count()):
            self.ui.target_categories.layout().itemAt(i).widget().deleteLater()

        self.reroll_colors()

        for i, category in enumerate(categories):
            wrap = QWidget(self.ui.menu)
            wrap.setLayout(QHBoxLayout())
            wrap.layout().setContentsMargins(0, 0, 0, 0)
            b = self._new_category_button(category, wrap)
            remove = self._new_remove_category_button(category, i, wrap)
            wrap.layout().addWidget(remove)
            wrap.layout().addWidget(b)
            self.ui.target_categories.addWidget(wrap)

    def _init_annotation_widgets(self):
        self._annotation_widget_old = AnnotationWidget(self.ui.target_old, self._framework.categories, self._category_colors,
                                                       self.annotations_changed, annotatable=False)
        self._annotation_widget_pred = AnnotationWidget(self.ui.target_pred, self._framework.categories, self._category_colors,
                                                        self.annotations_changed, annotatable=False)
        self._annotation_widget_new = AnnotationWidget(self.ui.target_new, self._framework.categories, self._category_colors,
                                                       self.annotations_changed, annotatable=True)

        self.ui.target_old.layout().addWidget(self._annotation_widget_old)
        self.ui.target_pred.layout().addWidget(self._annotation_widget_pred)
        self.ui.target_new.layout().addWidget(self._annotation_widget_new)

    def annotations_changed(self, load=False):
        self._framework.annotations_changed(load)
        self._list_annotations_new()
        self._annotation_widget_old.repaint()
        self._annotation_widget_pred.repaint()
        self._annotation_widget_new.repaint()

    def _connect_slots(self):
        self.ui.button_next.clicked.connect(self.load_next)
        self.ui.button_previous.clicked.connect(self.load_previous)
        self.ui.button_add_category.clicked.connect(self.add_category)
        self.ui.slider_score.valueChanged.connect(self.score_threshold_changed)
        self.ui.action_save.triggered.connect(self._framework.save)
        self.ui.action_reroll.triggered.connect(self.init_categories)
        self.ui.action_reset.triggered.connect(self.reset_reviewed)
        self.ui.checkbox_ai.toggled.connect(self.toggle_ai)
        self.ui.checkbox_skip.toggled.connect(self.toggle_skip)
        self.ui.checkBox_select.toggled.connect(self.toggle_select)
        self.ui.combobox_models.currentTextChanged.connect(self.model_changed)

    def load_next(self):
        data = self._framework.get_next_dataset()
        self._load_data(data)
        self.ui.button_previous.setDisabled(False)
        self.ui.button_next.setDisabled(data is None)

    def load_previous(self):
        data = self._framework.get_previous_dataset()
        self._load_data(data)
        self.ui.button_previous.setDisabled(data is None)
        self.ui.button_next.setDisabled(False)

    def _load_data(self, data: dict):
        self.ui.progressbar.setValue((self._framework.len_reviewed() / self._framework.len_new_files()) * 100)
        if data is None:
            self._annotation_widget_old.load_data(None, None)
            self._annotation_widget_new.load_data(None, None)
            self._annotation_widget_pred.load_data(None, None)
            self.window().setWindowTitle(f'anno-chan')
        else:
            self._set_panels_visibility()
            self.window().setWindowTitle(f'anno-chan :: {data["new"]["image"]["file_name"]}')
            qimage = ImageQt(data['new']['image_pil'].value)
            self._annotation_widget_old.load_data(data['old'], qimage)
            self._annotation_widget_new.load_data(data['new'], qimage)
            self._annotation_widget_pred.load_data(data['pred'], qimage)
            self.annotations_changed(load=True)

    def score_threshold_changed(self):
        self._annotation_widget_pred.score_threshold = self.ui.slider_score.value()/100
        self._framework.SCORE_THRESHOLD = self.ui.slider_score.value()/100
        self._annotation_widget_pred.repaint()

    def reroll_colors(self):
        self._category_colors.clear()
        rc = randomcolor.RandomColor()
        colors = rc.generate(count=len(self._framework.categories))
        for i, category in enumerate(self._framework.categories):
            self._category_colors[category['id']] = colors[i]

        self._annotation_widget_old.repaint()
        self._annotation_widget_new.repaint()
        self._annotation_widget_pred.repaint()
        self.repaint()

    def reset_reviewed(self):
        msgbox = QMessageBox()
        msgbox.setText(f'Reseting Reviewed Files"')
        msgbox.setInformativeText(
            "Do you really want to reset which files have been reviewed?")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        ret = msgbox.exec_()

        if ret == QMessageBox.Yes:
            self._framework.reset_reviewed()

    def toggle_ai(self):
        self._framework.AI_SUPPORT = self.ui.checkbox_ai.isChecked()
        self.ui.panel_pred.setVisible(self.ui.checkbox_ai.isChecked())
        self.ui.menu_pred.setVisible(self.ui.checkbox_ai.isChecked())
        self._set_panels_visibility()

    def toggle_select(self):
        self._framework.SELECT_PREDICTIONS = self.ui.checkBox_select.isChecked()

    def _set_panels_visibility(self):
        if self._framework.get_current_dataset() is None:
            return

        self.ui.panel_old.setVisible(self._framework.get_current_dataset()['old'] is not None)
        self.ui.panel_pred.setVisible(self.ui.checkbox_ai.isChecked())

        if self.ui.panel_old.isVisible() and self.ui.panel_pred.isVisible():
            self.ui.panel_panels.layout().setStretch(0, 1)
            self.ui.panel_panels.layout().setStretch(1, 1)

        if self.ui.panel_old.isVisible() or self.ui.panel_pred.isVisible():
            self.ui.panel_panels.setVisible(True)
            self.ui.layout_images.setStretch(0, 3)
            self.ui.layout_images.setStretch(1, 5)
        else:
            self.ui.panel_panels.setVisible(False)
            self.ui.layout_images.setStretch(0, 0)
            self.ui.layout_images.setStretch(1, 1)

    def toggle_skip(self):
        self._framework.SKIP_REVIEWED = self.ui.checkbox_skip.isChecked()

    def _list_annotations_new(self):
        data_new = self._framework.get_current_dataset()['new']
        model = QStandardItemModel(self.ui.list_new)
        model.appendRow(QStandardItem(f'{len(data_new["annotations"])} Annotations'))
        model.appendRow(QStandardItem(f'################################'))
        for i, annotation in enumerate(data_new['annotations']):
            item = QStandardItem(
                f'{annotation["category_id"]}:{[int(x*100)/100 for x in annotation["bbox"]]}::{round(data_new["scores"][i] * 100)}%')
            model.appendRow(item)
        self.ui.list_new.setModel(model)
        self.ui.list_new.update()

    def _get_category_button(self, category_id: int):
        return self.findChild(QPushButton, str(category_id))

    def select_category(self, *, category_id=None):
        category_id = self.sender().category_index if category_id is None else category_id
        self._annotation_widget_new.selected_category = category_id
        for i in range(self.ui.target_categories.layout().count()):
            self.ui.target_categories.layout().itemAt(i).widget().layout().itemAt(1).widget().setDisabled(False)
        self._get_category_button(category_id).setDisabled(True)
        self._annotation_widget_new.repaint()

    def remove_category(self):
        button_index = self.sender().button_index
        category_index = self.sender().category_index
        if category_index == 0:
            return

        category_name = [x['name'] for x in self._framework.categories if x['id'] == category_index][0]
        msgbox = QMessageBox()
        msgbox.setText(f'Deleting category "{category_name}"')
        msgbox.setInformativeText("Annotations with that category will NOT be removed!\n Do you really want to delete that category?")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        ret = msgbox.exec_()

        if ret == QMessageBox.Yes:
            if self._annotation_widget_new.selected_category == category_index:
                self._annotation_widget_new.selected_category = None
            del self._framework.categories[button_index]
            self.init_categories()

    def add_category(self):
        name = self.ui.textedit_category.toPlainText()
        index = max([x['id'] for x in self._framework.categories]) + 1 if len(self._framework.categories) > 0 else 1
        self._framework.categories.append({'id': index, 'name': name})
        self.ui.textedit_category.clearFocus()
        self.ui.textedit_category.clear()
        self.init_categories()

    def model_changed(self):
        self._framework.init_predictor(os.path.join('models/', self.ui.combobox_models.currentText()))
        self._framework.current_pred = None
        self._load_data(self._framework.get_current_dataset())

    def eventFilter(self, widget, event):
        if issubclass(type(event), QEvent) and event.type() == QtCore.QEvent.KeyPress:

            key = event.key()
            key_map = {QtCore.Qt.Key_AsciiCircum: 0, QtCore.Qt.Key_1: 1, QtCore.Qt.Key_2: 2, QtCore.Qt.Key_3: 3, QtCore.Qt.Key_4: 4,
                       QtCore.Qt.Key_5: 5, QtCore.Qt.Key_6: 6, QtCore.Qt.Key_7: 7, QtCore.Qt.Key_8: 8,
                       QtCore.Qt.Key_9: 9}

            if key == QtCore.Qt.Key_Space:
                self.load_next()
            else:
                for k in key_map.keys():
                    if key == k:
                        if key_map[key]  < len(self._framework.categories):
                            self.select_category(category_id=key_map[key])
            return True
        else:
            return False


if __name__ == "__main__":
    print('args:', sys.argv)
    app = QApplication(sys.argv)

    SAVE_RATE = 100
    root_path = None if len(sys.argv) < 2 else sys.argv[1]
    annotation_file_path = None if len(sys.argv) < 3 else sys.argv[2]
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
