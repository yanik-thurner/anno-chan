# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(803, 501)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_reroll = QAction(MainWindow)
        self.action_reroll.setObjectName(u"action_reroll")
        self.action_reset = QAction(MainWindow)
        self.action_reset.setObjectName(u"action_reset")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFocusPolicy(Qt.StrongFocus)
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.menu = QWidget(self.centralwidget)
        self.menu.setObjectName(u"menu")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMaximumSize(QSize(200, 16777215))
        self.menu.setStyleSheet(u"*{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(45, 50, 55);\n"
"}\n"
"QPushButton:disabled {\n"
"	background-color: rgb(30, 40, 40);\n"
"}\n"
"QPlainTextEdit{\n"
"	background-color: rgb(46, 52, 54);\n"
"}             \n"
"QLabel{\n"
"	font-weight: bold;\n"
"}    \n"
"#group_pred {\n"
"	background-color: rgb(55, 60, 65);\n"
"}  \n"
"\n"
"#group_pred  * {\n"
"	background-color: rgb(55, 60, 65);\n"
"}               \n"
"")
        self.menu_layout = QVBoxLayout(self.menu)
        self.menu_layout.setSpacing(6)
        self.menu_layout.setObjectName(u"menu_layout")
        self.menu_layout.setContentsMargins(6, -1, 6, -1)
        self.progressbar = QProgressBar(self.menu)
        self.progressbar.setObjectName(u"progressbar")
        self.progressbar.setValue(0)

        self.menu_layout.addWidget(self.progressbar)

        self.button_next = QPushButton(self.menu)
        self.button_next.setObjectName(u"button_next")
        self.button_next.setFocusPolicy(Qt.NoFocus)

        self.menu_layout.addWidget(self.button_next)

        self.button_previous = QPushButton(self.menu)
        self.button_previous.setObjectName(u"button_previous")
        self.button_previous.setEnabled(False)
        self.button_previous.setFocusPolicy(Qt.NoFocus)
        self.button_previous.setCheckable(False)

        self.menu_layout.addWidget(self.button_previous)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.menu_layout.addItem(self.verticalSpacer_2)

        self.categories_label = QLabel(self.menu)
        self.categories_label.setObjectName(u"categories_label")
        self.categories_label.setMaximumSize(QSize(150, 25))
        self.categories_label.setStyleSheet(u"")

        self.menu_layout.addWidget(self.categories_label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_add_category = QPushButton(self.menu)
        self.button_add_category.setObjectName(u"button_add_category")
        self.button_add_category.setMinimumSize(QSize(20, 20))
        self.button_add_category.setMaximumSize(QSize(20, 20))
        self.button_add_category.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_5.addWidget(self.button_add_category)

        self.textedit_category = QPlainTextEdit(self.menu)
        self.textedit_category.setObjectName(u"textedit_category")
        self.textedit_category.setMinimumSize(QSize(0, 32))
        self.textedit_category.setMaximumSize(QSize(16777215, 32))
        self.textedit_category.setFocusPolicy(Qt.ClickFocus)
        self.textedit_category.setStyleSheet(u"font-weight: normal; ")
        self.textedit_category.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.horizontalLayout_5.addWidget(self.textedit_category)


        self.menu_layout.addLayout(self.horizontalLayout_5)

        self.target_categories = QVBoxLayout()
        self.target_categories.setObjectName(u"target_categories")

        self.menu_layout.addLayout(self.target_categories)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.menu_layout.addItem(self.verticalSpacer)

        self.checkbox_skip = QCheckBox(self.menu)
        self.checkbox_skip.setObjectName(u"checkbox_skip")
        self.checkbox_skip.setFocusPolicy(Qt.NoFocus)
        self.checkbox_skip.setChecked(False)

        self.menu_layout.addWidget(self.checkbox_skip)

        self.group_pred = QWidget(self.menu)
        self.group_pred.setObjectName(u"group_pred")
        self.verticalLayout_6 = QVBoxLayout(self.group_pred)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.checkbox_ai = QCheckBox(self.group_pred)
        self.checkbox_ai.setObjectName(u"checkbox_ai")
        self.checkbox_ai.setMaximumSize(QSize(150, 16777215))
        self.checkbox_ai.setFocusPolicy(Qt.NoFocus)
        self.checkbox_ai.setIconSize(QSize(16, 16))
        self.checkbox_ai.setChecked(True)

        self.verticalLayout_6.addWidget(self.checkbox_ai)

        self.menu_pred = QWidget(self.group_pred)
        self.menu_pred.setObjectName(u"menu_pred")
        self.verticalLayout_3 = QVBoxLayout(self.menu_pred)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkBox_select = QCheckBox(self.menu_pred)
        self.checkBox_select.setObjectName(u"checkBox_select")
        self.checkBox_select.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_3.addWidget(self.checkBox_select)

        self.label_4 = QLabel(self.menu_pred)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.label_4)

        self.slider_score = QSlider(self.menu_pred)
        self.slider_score.setObjectName(u"slider_score")
        self.slider_score.setFocusPolicy(Qt.NoFocus)
        self.slider_score.setMaximum(100)
        self.slider_score.setSingleStep(5)
        self.slider_score.setValue(70)
        self.slider_score.setTracking(True)
        self.slider_score.setOrientation(Qt.Horizontal)
        self.slider_score.setInvertedAppearance(False)
        self.slider_score.setInvertedControls(False)
        self.slider_score.setTickPosition(QSlider.TicksBelow)
        self.slider_score.setTickInterval(0)

        self.verticalLayout_3.addWidget(self.slider_score)

        self.combobox_models = QComboBox(self.menu_pred)
        self.combobox_models.setObjectName(u"combobox_models")
        self.combobox_models.setFocusPolicy(Qt.NoFocus)
        self.combobox_models.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)

        self.verticalLayout_3.addWidget(self.combobox_models)


        self.verticalLayout_6.addWidget(self.menu_pred)


        self.menu_layout.addWidget(self.group_pred)


        self.horizontalLayout_6.addWidget(self.menu)

        self.layout_images = QVBoxLayout()
        self.layout_images.setObjectName(u"layout_images")
        self.panel_panels = QWidget(self.centralwidget)
        self.panel_panels.setObjectName(u"panel_panels")
        self.horizontalLayout = QHBoxLayout(self.panel_panels)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.panel_old = QWidget(self.panel_panels)
        self.panel_old.setObjectName(u"panel_old")
        self.pane_old = QVBoxLayout(self.panel_old)
        self.pane_old.setSpacing(0)
        self.pane_old.setObjectName(u"pane_old")
        self.pane_old.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.panel_old)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 15))

        self.pane_old.addWidget(self.label_2)

        self.target_old = QFrame(self.panel_old)
        self.target_old.setObjectName(u"target_old")
        self.target_old.setCursor(QCursor(Qt.ArrowCursor))
        self.target_old.setFrameShape(QFrame.StyledPanel)
        self.target_old.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.target_old)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.pane_old.addWidget(self.target_old)


        self.horizontalLayout.addWidget(self.panel_old)

        self.panel_pred = QWidget(self.panel_panels)
        self.panel_pred.setObjectName(u"panel_pred")
        self.panel_pred.setEnabled(True)
        self.pane_pred = QVBoxLayout(self.panel_pred)
        self.pane_pred.setSpacing(0)
        self.pane_pred.setObjectName(u"pane_pred")
        self.pane_pred.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.panel_pred)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMaximumSize(QSize(16777215, 15))

        self.pane_pred.addWidget(self.label_3)

        self.target_pred = QFrame(self.panel_pred)
        self.target_pred.setObjectName(u"target_pred")
        self.target_pred.setCursor(QCursor(Qt.ArrowCursor))
        self.target_pred.setFrameShape(QFrame.StyledPanel)
        self.target_pred.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.target_pred)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.pane_pred.addWidget(self.target_pred)


        self.horizontalLayout.addWidget(self.panel_pred)


        self.layout_images.addWidget(self.panel_panels)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 15))
        self.label.setTextFormat(Qt.AutoText)

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.target_new = QFrame(self.centralwidget)
        self.target_new.setObjectName(u"target_new")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.target_new.sizePolicy().hasHeightForWidth())
        self.target_new.setSizePolicy(sizePolicy2)
        self.target_new.setFrameShape(QFrame.StyledPanel)
        self.target_new.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.target_new)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_8.addWidget(self.target_new)

        self.list_new = QListView(self.centralwidget)
        self.list_new.setObjectName(u"list_new")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.list_new.sizePolicy().hasHeightForWidth())
        self.list_new.setSizePolicy(sizePolicy3)
        self.list_new.setMinimumSize(QSize(310, 0))
        self.list_new.setMaximumSize(QSize(310, 16777215))
        font = QFont()
        font.setFamily(u"FreeMono")
        font.setPointSize(11)
        self.list_new.setFont(font)
        self.list_new.setFocusPolicy(Qt.NoFocus)
        self.list_new.setProperty("isWrapping", True)
        self.list_new.setLayoutMode(QListView.Batched)
        self.list_new.setViewMode(QListView.ListMode)
        self.list_new.setWordWrap(True)

        self.horizontalLayout_8.addWidget(self.list_new)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.layout_images.addLayout(self.verticalLayout_4)

        self.layout_images.setStretch(0, 3)
        self.layout_images.setStretch(1, 5)

        self.horizontalLayout_6.addLayout(self.layout_images)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 803, 29))
        self.menuDataset = QMenu(self.menubar)
        self.menuDataset.setObjectName(u"menuDataset")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuDataset.menuAction())
        self.menuDataset.addAction(self.action_open)
        self.menuDataset.addAction(self.action_save)
        self.menuDataset.addSeparator()
        self.menuDataset.addAction(self.action_reroll)
        self.menuDataset.addAction(self.action_reset)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"anno-chan", None))
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_reroll.setText(QCoreApplication.translate("MainWindow", u"Reroll Colors", None))
        self.action_reset.setText(QCoreApplication.translate("MainWindow", u"Reset Reviewed", None))
        self.button_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.button_previous.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.categories_label.setText(QCoreApplication.translate("MainWindow", u"Categories", None))
        self.button_add_category.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.textedit_category.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Category Name", None))
        self.checkbox_skip.setText(QCoreApplication.translate("MainWindow", u"Skip Reviewed", None))
        self.checkbox_ai.setText(QCoreApplication.translate("MainWindow", u"AI Support", None))
        self.checkBox_select.setText(QCoreApplication.translate("MainWindow", u"Select Predictions", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Score Threshold", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Old Annotations", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Predicted Annotations", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"New Annotations", None))
        self.menuDataset.setTitle(QCoreApplication.translate("MainWindow", u"Dataset", None))
    # retranslateUi

