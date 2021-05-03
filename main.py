#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.convert)
        self.comboBox.clear()
        list1 = [self.tr('First Item'),
                 self.tr('Second Item'),
                 self.tr('Third Item'),
                 self.tr('LOOOOOOOONG CAT')]
        self.comboBox.addItems(list1)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def convert(self):
        text = 'encode' if self.radio_encode.isChecked() else 'decode'
        text += self.comboBox.currentText()
        self.textEdit.setText(text)
        # self.textEdit.setText("OK")
        # Имя элемента совпадает с objectName в QTDesigner


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
