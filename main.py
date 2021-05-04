#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import hashlib
from inspect import signature
import json

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

import coders


CONFIG_FILE = 'config.json'


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.convert_button.clicked.connect(self.convert)
        self.radio_encode.toggled.connect(self.switch_mode_callback)
        self.radio_decode.toggled.connect(self.switch_mode_callback)
        self.radio_hash.toggled.connect(self.switch_mode_callback)
        self.coding_selector.currentTextChanged\
            .connect(self.switch_algorithm_callback)

        self.coders_list = coders.CODERS
        self.decoders_list = coders.DECODERS
        algs = hashlib.algorithms_available
        self.hashes_list = [str(hs) for hs in sorted(list(algs))]

        self.load_params()
        self.set_drop_down_coders()
        self.hide_error()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and \
           event.key() == Qt.Key_Q:
            sys.exit()
        if event.key() == Qt.Key_Escape:
            sys.exit()

    def closeEvent(self, event):
        self.save_params()

    def save_params(self):
        self.params['geometry'] = self.geometry().getRect()
        with open(CONFIG_FILE, 'w') as fp:
            json.dump(self.params, fp)

    def load_params(self):
        try:
            with open(CONFIG_FILE, 'r') as fp:
                self.params = json.load(fp)
        except FileNotFoundError:
            self.params = dict()
        if 'geometry' in self.params:
            self.setGeometry(*self.params['geometry'])

    def switch_mode_callback(self, event):
        if self.radio_encode.isChecked():
            self.set_drop_down_coders()
        elif self.radio_decode.isChecked():
            self.set_drop_down_decoders()
        elif self.radio_hash.isChecked():
            self.set_drop_down_hashes()

    def switch_algorithm_callback(self, event):
        self.hile_key_spin()
        self.hile_key_field()

        if self.radio_encode.isChecked() and event in self.coders_list:
            self.params['last_coder'] = event
            if coders.is_key(event) == coders.KEY_DECIMAL:
                self.show_key_spin()
            elif coders.is_key(event) == coders.KEY_TEXT:
                self.show_key_field()

        elif self.radio_decode.isChecked() and event in self.decoders_list:
            self.params['last_decoder'] = event
            if coders.is_key(event) == coders.KEY_DECIMAL:
                self.show_key_spin()
            elif coders.is_key(event) == coders.KEY_TEXT:
                self.show_key_field()

        elif event in self.hashes_list:
            self.params['last_hash'] = event

    def get_md(self, string, algorithm):
        hash_obj = hashlib.new(algorithm, string.encode('utf-8'))
        if len(signature(hash_obj.hexdigest).parameters) == 0:
            return hash_obj.hexdigest()
        else:
            return hash_obj.hexdigest(1024)

    def encode(self, string, algorithm, key=None):
        error, text = coders.encode(string, algorithm, key)
        if error:
            self.show_error(error['title'], error['text'])
        return text

    def decode(self, string, algorithm, key=None):
        error, text = coders.decode(string, algorithm, key)
        if error:
            self.show_error(error['title'], error['text'])
        return text

    def convert(self):
        self.hide_error()
        key_type = coders.is_key(self.coding_selector.currentText())
        key = None
        if key_type == coders.KEY_DECIMAL:
            key = self.key_spin.value()
        elif key_type == coders.KEY_TEXT:
            key = self.key_field.text()

        if self.radio_encode.isChecked():
            text = self.encode(self.text_field.toPlainText(),
                               self.coding_selector.currentText(),
                               key)

        elif self.radio_decode.isChecked():
            text = self.decode(self.text_field.toPlainText(),
                               self.coding_selector.currentText(),
                               key)

        elif self.radio_hash.isChecked():
            text = self.get_md(self.text_field.toPlainText(),
                               self.coding_selector.currentText())

        else:
            raise ZeroDivisionError('Oh shi~')

        self.text_field.setPlainText(text)

    def show_key_spin(self):
        self.hile_key_field()
        self.key_label.show()
        self.key_spin.show()

    def hile_key_spin(self):
        self.key_label.hide()
        self.key_spin.hide()

    def show_key_field(self):
        self.hile_key_spin()
        self.key_label.show()
        self.key_field.show()

    def hile_key_field(self):
        self.key_label.hide()
        self.key_field.hide()

    def set_drop_down_coders(self):
        index = 0
        if 'last_coder' in self.params:
            index = self.coders_list.index(self.params['last_coder'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.coders_list)
        self.coding_selector.setCurrentIndex(index)

    def set_drop_down_decoders(self):
        index = 0
        if 'last_coder' in self.params:
            index = self.decoders_list.index(self.params['last_decoder'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.decoders_list)
        self.coding_selector.setCurrentIndex(index)

    def set_drop_down_hashes(self):
        index = 0
        if 'last_coder' in self.params:
            index = self.hashes_list.index(self.params['last_hash'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.hashes_list)
        self.coding_selector.setCurrentIndex(index)

    def hide_error(self):
        self.error_label.hide()

    def show_error(self, error_title, error_text):
        self.error_label.setText(error_title)
        self.error_label.setToolTip(error_text)
        self.error_label.setStyleSheet("color: red")
        self.error_label.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWidget()
    main_window.show()
    sys.exit(app.exec_())
