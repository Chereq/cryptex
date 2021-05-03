#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.convert_button.clicked.connect(self.convert)
        self.radio_encode.toggled.connect(self.switch_mode_callback)
        self.radio_decode.toggled.connect(self.switch_mode_callback)
        self.radio_hash.toggled.connect(self.switch_mode_callback)

        self.coders_list = [self.tr('Encode1'),
                            self.tr('Encode2'),
                            self.tr('Encode3'),
                            self.tr('Encode4')]

        self.decoders_list = [self.tr('Decode1'),
                              self.tr('Decode2'),
                              self.tr('Decode3'),
                              self.tr('Decode4')]

        self.hashes_list = [self.tr('Hash1'),
                            self.tr('Hash2'),
                            self.tr('Hash3'),
                            self.tr('Hash4')]

        self.set_drop_down_coders()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            sys.exit()

    def switch_mode_callback(self, event):
        if self.radio_encode.isChecked():
            self.set_drop_down_coders()
        elif self.radio_decode.isChecked():
            self.set_drop_down_decoders()
        elif self.radio_hash.isChecked():
            self.set_drop_down_hashes()

    def convert(self):
        text = ''
        if self.radio_encode.isChecked():
            text += 'encode'
        elif self.radio_decode.isChecked():
            text += 'decode'
        elif self.radio_hash.isChecked():
            text += 'hash'
        else:
            raise ZeroDivisionError('Oh shi~')
        text += self.coding_selector.currentText()
        self.text_field.setPlainText(text)

    def show_key_field(self):
        self.key_label.show()
        self.key_field.show()

    def hile_key_field(self):
        self.key_label.hide()
        self.key_field.hide()

    def set_drop_down_coders(self):
        self.show_key_field()
        self.coding_selector.clear()
        self.coding_selector.addItems(self.coders_list)

    def set_drop_down_decoders(self):
        self.show_key_field()
        self.coding_selector.clear()
        self.coding_selector.addItems(self.decoders_list)

    def set_drop_down_hashes(self):
        self.hile_key_field()
        self.coding_selector.clear()
        self.coding_selector.addItems(self.hashes_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWidget()
    main_window.show()
    sys.exit(app.exec_())
