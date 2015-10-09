#!/usr/bin/env python3

import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import(
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFormLayout, QListWidget, QListWidgetItem,
    QLineEdit)


class requester(QWidget):

    def __init__(self):
        super(requester, self).__init__()
        self.path = "/"
        self.main_Layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.main_Layout.setContentsMargins(5, 5, 5, 5)
        self.main_Layout.setSpacing(5)
        self.myQListWidget = QListWidget(self)
        self.myQListWidget.setStyleSheet("""
            QListWidget:item:selected:active {
            background-color:#A6A4FF;}
            """)

        self.ok_button = ok_button(parent=self)
        self.volumes_button = volumes_button(parent=self)
        self.parent_button = parent_button(parent=self)
        self.cancel_button = cancel_button()

        self.drawer_field = drawer_field()
        self.file_field = file_field()
        
        self.form_layout.addRow("Drawer", self.drawer_field)
        self.form_layout.addRow("File", self.file_field)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.volumes_button)
        self.button_layout.addWidget(self.parent_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_Layout.addWidget(self.myQListWidget)
        self.main_Layout.addLayout(self.form_layout)
        self.main_Layout.addLayout(self.button_layout)
        self.setLayout(self.main_Layout)
        self.create_list(self.path)

    def create_list(self, path):
        self.myQListWidget.clear()
        for item in os.listdir(path):
            # print(item)
            if os.path.isdir(os.path.join(path, item)):
                self.myQCustomQWidget = QCustomQWidget(name=item,
                                                       kind="Drawer",
                                                       path=path,
                                                       parent=self)
                myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())
                self.myQListWidget.addItem(myQListWidgetItem)
                self.myQListWidget.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)
        for item in os.listdir(path):
            if os.path.isfile(os.path.join(path, item)):
                self.myQCustomQWidget = QCustomQWidget(name=item,
                                                       kind="file", 
                                                       path=path, 
                                                       parent=self)
                myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())
                self.myQListWidget.addItem(myQListWidgetItem)
                self.myQListWidget.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)


class QCustomQWidget (QWidget):

    def __init__(self, name=None, kind=None, path=None, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.path = path
        self.parent = parent
        self.file_layout = QHBoxLayout()
        self.file_layout.setContentsMargins(5, 5, 5, 0)
        # self.file_layout.setSpacing(10)
        self.name_label = QLabel("")
        self.kind_label = QLabel("")
        self.kind_label.setAlignment(Qt.AlignRight)
        self.file_layout.addWidget(self.name_label)
        self.file_layout.addWidget(self.kind_label)
        self.file_layout.addSpacing(5)
        self.setLayout(self.file_layout)
        self.kind = kind
        self.name = name
        self.set_text(name)

    def set_text(self, text):
        if self.kind == "Drawer":
            self.setStyleSheet('''color: rgb(0, 0, 255);''')
            self.kind_label.setText(self.kind)
        else:
            self.setStyleSheet('''color: rgb(0, 0, 0);''')        
        self.name_label.setText(self.name)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # print("path=", self.path)
            self.parent.path = self.path
            self.parent.create_list(path=os.path.join(self.path, self.name))


class drawer_field(QLineEdit):

    def __init__(self, name=None, kind=None, parent=None):
        super(drawer_field, self).__init__(parent)
        pass


class file_field(QLineEdit):

    def __init__(self, name=None, kind=None, parent=None):
        super(file_field, self).__init__(parent)
        pass


class ok_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(ok_button, self).__init__(parent)
        self.setText("Ok")
        self.show()


class volumes_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(volumes_button, self).__init__(parent)
        self.parent = parent
        self.setText("Volumes")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.create_list(path="/Volumes/")


class parent_button(QPushButton):

    def __init__(self, name=None, kind=None, path=None, parent=None):
        super(parent_button, self).__init__(parent)
        self.parent = parent
        self.path = path
        self.setText("Parent")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # print(self.parent.path)
            self.parent.create_list(path=self.parent.path)


class cancel_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(cancel_button, self).__init__(parent)
        self.setText("Cancel")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            sys.exit(0)


if __name__ == '__main__':
    app = QApplication([])
    window = requester()
    window.show()
    sys.exit(app.exec_())
